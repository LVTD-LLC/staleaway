from unittest.mock import patch

import pytest
from django.urls import reverse

from core import tasks
from core.models import Page, Sitemap


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["landing_page", "pricing", "account_login", "account_signup"])
def test_public_pages_use_staleaway(client, name):
    response = client.get(reverse(name))
    assert response.status_code == 200
    text = response.content.decode()
    assert "Staleaway" in text
    assert "Cleanapp" not in text and "PageFresh" not in text


@pytest.mark.django_db
def test_restored_import_keeps_metadata_columns(auth_client, profile):
    with patch("core.views.async_task"):
        response = auth_client.post(
            reverse("home"), {"sitemap_url": "https://example.com/sitemap.xml"}
        )
    assert response.status_code == 302
    sitemap = Sitemap.objects.get(profile=profile)
    assert sitemap.client_label == ""
    assert sitemap.import_status == "pending"
    page = Page.objects.create(profile=profile, sitemap=sitemap, url="https://example.com/about")
    assert page.review_outcome == "pending"
    assert page.review_note == ""


@pytest.mark.django_db
def test_review_link_preserves_saved_metadata(auth_client, profile):
    sitemap = Sitemap.objects.create(
        profile=profile, sitemap_url="https://example.com/sitemap.xml", client_label="Saved client"
    )
    page = Page.objects.create(
        profile=profile,
        sitemap=sitemap,
        url="https://example.com/about",
        review_note="Saved note",
        review_outcome="needs_follow_up",
    )
    response = auth_client.get(reverse("review_page_redirect", args=[page.pk]))
    assert response.status_code == 302
    assert response.url == page.url
    page.refresh_from_db()
    assert page.reviewed and page.reviewed_at
    assert page.review_note == "Saved note"
    assert page.review_outcome == "needs_follow_up"
    assert sitemap.client_label == "Saved client"


@pytest.mark.django_db
def test_review_link_cannot_change_other_users_page(auth_client, django_user_model):
    other = django_user_model.objects.create_user(username="other", email="other@example.com")
    page = Page.objects.create(profile=other.profile, url="https://example.com/private")
    response = auth_client.get(reverse("review_page_redirect", args=[page.pk]))
    assert response.url == reverse("home")
    page.refresh_from_db()
    assert not page.reviewed


@pytest.mark.django_db
def test_email_restores_page_selection_and_template_context(profile, settings, mailoutbox):
    settings.SITE_URL = "https://staleaway.com"
    sitemap = Sitemap.objects.create(
        profile=profile, sitemap_url="https://example.com/sitemap.xml", pages_per_review=2
    )
    expected = Page.objects.create(
        profile=profile, sitemap=sitemap, url="https://example.com/about"
    )
    Page.objects.create(
        profile=profile, sitemap=sitemap, url="https://example.com/reviewed", reviewed=True
    )
    Page.objects.create(
        profile=profile, sitemap=sitemap, url="https://example.com/excluded", needs_review=False
    )
    from django.template.loader import render_to_string

    def render_without_network(name, context):
        # Exercise the full restored template and context, replacing only the remote MJML compiler.
        with patch("mjml.templatetags.mjml.mjml_render", side_effect=lambda source: source):
            return render_to_string(name, context)

    with (
        patch.object(tasks, "fetch_page_metadata", return_value={"title": "About us"}),
        patch("django.template.loader.render_to_string", side_effect=render_without_network),
    ):
        result = tasks.send_page_email_to_profile(profile.pk)
    assert result.startswith("Successfully sent")
    assert len(mailoutbox) == 1
    html = mailoutbox[0].alternatives[0].content
    assert f"https://staleaway.com/review-page/{expected.pk}/" in html
    assert "About us" in html
    assert "Staleaway" in html
    assert "/excluded" not in html and "/reviewed" not in html
    expected.refresh_from_db()
    assert not expected.reviewed


@pytest.mark.django_db
def test_removed_agent_api_is_not_exposed(auth_client):
    assert auth_client.get("/api/sites").status_code == 404


def test_checkout_plan_contract(settings):
    from core.views import get_price_id_for_plan

    settings.STRIPE_PRICE_IDS = {"monthly": "price_month", "yearly": "price_year"}
    assert get_price_id_for_plan("monthly") == "price_month"
    assert get_price_id_for_plan("yearly") == "price_year"
    assert get_price_id_for_plan("agency") is None
