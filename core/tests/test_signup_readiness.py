import re

import pytest

from core.choices import BlogPostStatus
from core.models import BlogPost
from core.tests.test_analytics_privacy import analytics_config

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("status", [None, BlogPostStatus.DRAFT, BlogPostStatus.PUBLISHED])
@pytest.mark.parametrize("invalid_post", [False, True])
def test_signup_help_is_published_only_and_keeps_auth_boundary(
    client, settings, django_user_model, status, invalid_post
):
    settings.POSTHOG_API_KEY = "synthetic-public-project-key"
    if status is not None:
        BlogPost.objects.create(
            title="Find your sitemap", slug="find-your-website-sitemap",
            content="Public fixture", tags="", status=status,
        )
    before = django_user_model.objects.count()
    if invalid_post:
        response = client.post("/accounts/signup/", {
            "username": "readiness-preview", "email": "reader@example.invalid",
            "password1": "", "password2": "", "next": "/home",
        })
        assert response.context["form"].errors
        assert response.context["form"]["username"].value() == "readiness-preview"
        assert response.context["form"]["email"].value() == "reader@example.invalid"
        assert 'name="next" value="/home"' in response.content.decode()
    else:
        response = client.get("/accounts/signup/", {"next": "/home"})
    assert response.status_code == 200
    assert django_user_model.objects.count() == before
    html = response.content.decode()
    assert analytics_config(response) is None
    assert "posthog.init" not in html
    assert 'name="csrfmiddlewaretoken"' in html
    assert '<form class="mt-8 space-y-6" id="signup_form" method="post" action="/accounts/signup/">' in html
    assert "You can create your account before finding your sitemap." in html
    help_links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*target="_blank" rel="noopener noreferrer"', html)
    assert "/#how-it-works" in help_links
    assert ("/blog/find-your-website-sitemap" in help_links) == (status == BlogPostStatus.PUBLISHED)
    assert all("next=" not in link for link in help_links)


def test_signup_fields_have_distinct_visible_names_and_creation_autocomplete(client):
    html = client.get("/accounts/signup/").content.decode()
    assert len(re.findall(r"<h1\b", html)) == 1
    for field, label in [
        ("username", "Username"), ("email", "Email"),
        ("password1", "Password"), ("password2", "Confirm password"),
    ]:
        match = re.search(r'<label for="' + field + r'" class="([^"]*)">([^<]+)</label>', html)
        assert match and match.group(2) == label
        assert "sr-only" not in match.group(1).split()
    for field in ["password1", "password2"]:
        tag = re.search(r'<input[^>]*id="' + field + r'"[^>]*>', html).group()
        assert 'autocomplete="new-password"' in tag
        assert 'type="password"' in tag
