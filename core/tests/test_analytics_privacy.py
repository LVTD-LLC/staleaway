import json
import re
from unittest.mock import Mock

import pytest
from django.urls import reverse
from allauth.account.models import EmailAddress

from core.choices import BlogPostStatus
from core.models import BlogPost
from core.tasks import track_event, try_create_posthog_alias

pytestmark = pytest.mark.django_db


def analytics_config(response):
    match = re.search(
        r'<script id="public-analytics-config" type="application/json">(.*?)</script>',
        response.content.decode(),
        re.S,
    )
    return json.loads(match.group(1)) if match else None


@pytest.mark.parametrize("path", ["/", "/blog", "/uses"])
def test_only_canonical_public_url_reaches_collector(client, settings, path):
    settings.POSTHOG_API_KEY = "synthetic-public-project-key"
    settings.SITE_URL = "http://testserver"
    response = client.get(path, {"next": "/review-page/123/?token=private-marker"})
    assert response.status_code == 200
    config = analytics_config(response)
    assert config == {"api_key": settings.POSTHOG_API_KEY, "url": "http://testserver" + path}
    html = response.content.decode()
    assert "posthog.init" not in html
    assert "script.outbound-links" not in html


@pytest.mark.parametrize(
    "path",
    [
        "/accounts/login/", "/accounts/signup/", "/accounts/password/reset/",
        "/accounts/password/reset/key/invalid-key/", "/accounts/confirm-email/invalid-key/",
        "/home", "/settings", "/review-page/123/", "/sitemap/123",
        "/blog/missing-private-marker", "/missing-private-marker",
    ],
)
def test_private_auth_redirect_and_error_responses_have_no_analytics(client, settings, path):
    settings.POSTHOG_API_KEY = "synthetic-public-project-key"
    response = client.get(path, {"next": "/review-page/123/?token=private-marker"}, follow=True)
    assert analytics_config(response) is None
    html = response.content.decode()
    assert "posthog.init" not in html
    assert "script.outbound-links" not in html


@pytest.mark.parametrize("path", ["/", "/blog", "/uses", "/home", "/settings"])
def test_authenticated_pages_have_no_browser_measurement(auth_client, settings, path):
    settings.POSTHOG_API_KEY = "synthetic-public-project-key"
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(username="testuser")
    EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
    response = auth_client.get(path)
    assert response.status_code == 200
    assert analytics_config(response) is None
    assert "posthog.init" not in response.content.decode()
    assert "script.outbound-links" not in response.content.decode()


def test_only_published_article_is_measured(client, settings):
    settings.POSTHOG_API_KEY = "synthetic-public-project-key"
    post = BlogPost.objects.create(title="Draft", slug="draft", content="Body", tags="")
    assert analytics_config(client.get(post.get_absolute_url())) is None
    post.status = BlogPostStatus.PUBLISHED
    post.save()
    assert analytics_config(client.get(post.get_absolute_url()))["url"].endswith("/blog/draft")


def test_missing_key_is_measurement_off(client, settings):
    settings.POSTHOG_API_KEY = ""
    assert analytics_config(client.get("/")) is None


def test_queued_alias_is_noop_even_with_private_legacy_cookie(monkeypatch, profile):
    alias = Mock()
    log = Mock()
    monkeypatch.setattr("core.tasks.posthog.alias", alias)
    monkeypatch.setattr("core.tasks.logger", log)
    assert try_create_posthog_alias(profile.pk, {"sessionid": "private-cookie"})
    alias.assert_not_called()
    assert not log.mock_calls


def test_signup_measurement_ignores_legacy_properties(monkeypatch, profile, settings):
    settings.POSTHOG_API_KEY = "synthetic-public-project-key"
    settings.SITE_URL = "https://staleaway.com"
    capture = Mock()
    monkeypatch.setattr("core.tasks.posthog.capture", capture)
    private = {
        "$set": {"email": profile.user.email, "username": profile.user.username},
        "$current_url": "https://private.invalid/review?token=private-marker",
        "$host": "private.invalid", "$process_person_profile": True,
    }
    track_event(profile.pk, "user_signed_up", private)
    args, kwargs = capture.call_args
    assert re.fullmatch(r"account_[a-f0-9]{64}", args[0])
    assert kwargs == {
        "event": "user_signed_up",
        "properties": {
            "$host": "staleaway.com", "$process_person_profile": False,
            "$geoip_disable": True, "measurement_version": "public-v1", "source": "server",
        },
    }
    assert profile.user.email not in json.dumps([args, kwargs])
    track_event(profile.pk, "user_signed_up", {})
    assert capture.call_args[0][0] == args[0]
    capture.reset_mock()
    track_event(profile.pk, "private-event", private)
    capture.assert_not_called()


def test_retained_signup_hook_does_not_queue_cookies_or_identity_properties(monkeypatch):
    from allauth.account.views import SignupView
    from django.contrib.auth.models import AnonymousUser
    from django.http import HttpResponse
    from django.test import RequestFactory

    from core.views import AccountSignupView

    # Exercise the project's successful-signup hook without sending any email.
    queued = Mock()
    monkeypatch.setattr("core.views.async_task", queued)
    monkeypatch.setattr(SignupView, "form_valid", lambda self, form: HttpResponse("created"))
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.create_user(username="signup-test", email="signup@example.invalid")
    view = AccountSignupView()
    view.request = RequestFactory().post(reverse("account_signup"))
    view.request.user = AnonymousUser()
    view.request.COOKIES = {"sessionid": "private-session-marker"}
    view.user = user
    assert view.form_valid(Mock()).status_code == 200
    queued.assert_called_once()
    assert queued.call_args[0][0] == "core.tasks.track_event"
    assert queued.call_args[1]["properties"] == {}
    assert "private-session-marker" not in str(queued.call_args)
