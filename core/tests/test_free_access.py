from unittest.mock import patch

import pytest
from allauth.account.models import EmailAddress
from django.urls import reverse

from core.choices import ProfileStates
from core.models import Page, Sitemap


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    [
        "/pricing",
        "/stripe/webhook/",
        "/create-checkout-session/1/monthly/",
        "/create-customer-portal/",
        "/api/user/settings",
    ],
)
def test_billing_endpoints_removed(auth_client, path):
    assert auth_client.get(path).status_code == 404
    assert auth_client.post(path).status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("state", ProfileStates.values)
def test_all_features_free_regardless_of_historical_state(auth_client, profile, state):
    profile.state = state
    profile.save(update_fields=["state"])
    EmailAddress.objects.create(
        user=profile.user, email=profile.user.email, verified=True, primary=True
    )
    with patch("core.views.async_task"):
        response = auth_client.post(
            reverse("home"), {"sitemap_url": "https://example.com/sitemap.xml"}
        )
    assert response.status_code == 302
    sitemap = Sitemap.objects.get(profile=profile)
    response = auth_client.post(
        reverse("settings"),
        {
            "timezone": "Europe/London",
            "preferred_email_time": "09:30",
            f"sitemap_{sitemap.pk}-pages_per_review": 10,
            f"sitemap_{sitemap.pk}-review_cadence": "weekly",
        },
    )
    assert response.status_code == 302
    sitemap.refresh_from_db()
    assert sitemap.pages_per_review == 10 and sitemap.review_cadence == "weekly"
    response = auth_client.post(
        "/api/emails/add", {"email_address": "extra@example.com"}, content_type="application/json"
    )
    assert response.json()["success"]
    page = Page.objects.create(profile=profile, sitemap=sitemap, url="https://example.com/about")
    assert auth_client.get(reverse("review_page_redirect", args=[page.pk])).url == page.url
    for name in ["landing_page", "home", "settings", "account_signup"]:
        response = auth_client.get(reverse(name))
        assert response.status_code in [200, 302]
        content = response.content.decode().lower()
        assert "stripe" not in content and "pricing" not in content
        assert "subscription" not in content and "checkout" not in content
    profile.refresh_from_db()
    assert profile.state == state


@pytest.mark.django_db
def test_landing_advertises_free_access(client):
    response = client.get(reverse("landing_page") + "?payment=success")
    text = response.content.decode()
    assert "All features are free" in text
    assert "Thanks for subscribing" not in text
    assert "/pricing" not in client.get("/sitemap.xml").content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("state", ProfileStates.values)
def test_reminders_scheduled_for_every_historical_state(profile, state):
    from datetime import datetime, timezone
    from core import tasks

    profile.state = state
    profile.save(update_fields=["state"])
    Sitemap.objects.create(profile=profile, sitemap_url="https://example.com/sitemap.xml")
    with (
        patch.object(
            tasks.timezone, "now", return_value=datetime(2026, 10, 4, 9, 0, tzinfo=timezone.utc)
        ),
        patch.object(tasks, "async_task") as queue,
    ):
        result = tasks.schedule_review_emails()
    assert result == "Checked 1 profiles, scheduled 1 emails"
    queue.assert_called_once_with(
        "core.tasks.send_page_email_to_profile", profile_id=profile.pk, group="Email Scheduling"
    )
