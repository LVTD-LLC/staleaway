import json
import re
from xml.etree import ElementTree

import pytest
from django.urls import reverse

from core.choices import BlogPostStatus
from core.models import BlogPost, Page, Sitemap
from core.tests.test_analytics_privacy import analytics_config
from core.tests.test_public_seo import schemas

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("name", ["tools", "content_review_planner"])
def test_public_tool_metadata_and_schema(client, settings, name):
    settings.SITE_URL = "https://canonical.example"
    path = reverse(name)
    response = client.get(path)
    assert response.status_code == 200
    html = response.content.decode()
    assert len(re.findall(r'<link rel="canonical"', html)) == 1
    assert f'<link rel="canonical" href="https://canonical.example{path}"' in html
    title = re.search(r"<title>(.*?)</title>", html).group(1)
    description = re.search(r'<meta name="description" content="(.*?)"', html).group(1)
    assert len(title) <= 60
    assert len(description) <= 155
    assert "noindex" not in html
    data = schemas(response)
    assert data[0]["url"] == "https://canonical.example" + path
    assert data[1]["@type"] == "BreadcrumbList"
    assert data[1]["itemListElement"][-1]["item"] == "https://canonical.example" + path
    if name == "content_review_planner":
        assert data[0]["@type"] == "WebApplication"
        assert data[0]["offers"] == {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
        assert data[0]["isAccessibleForFree"] is True
        assert data[0]["dateModified"] == "2026-10-21"
        assert "Content review workload planner" in html
        assert 'data-controller="review-planner"' in html
        assert '<fieldset disabled data-review-planner-target="fields">' in html
        assert 'data-review-planner-target="result" hidden' in html
        assert "No estimate has been calculated" in html
        assert "<noscript>" in html
        assert 'maxlength="6"' not in html
        assert "keydown.enter->review-planner#calculate" in html
        assert "manual" in html.lower()
        for key in ["pages", "minutesPerPage", "sessionMinutes", "sessionsPerWeek", "targetWeeks"]:
            assert f'for="planner-{key}"' in html
            assert f'aria-describedby="planner-{key}-hint planner-{key}-error"' in html
        assert 'data-review-planner-target="breakdown"></dl>' in html


def test_tools_are_discoverable_without_blog_fixtures(client):
    planner = reverse("content_review_planner")
    nonprofit = reverse("for_nonprofits")
    for path in ["/", "/blog", "/tools"]:
        response = client.get(path)
        assert response.status_code == 200
        html = response.content.decode()
        assert f'href="{planner}"' in html
        assert 'href="/tools"' in html
        if path in {"/", "/tools"}:
            assert f'href="{nonprofit}"' in html
    sitemap = client.get("/sitemap.xml")
    assert sitemap.status_code == 200
    root = ElementTree.fromstring(sitemap.content)
    locations = [element.text for element in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    assert sum(url.endswith(planner) for url in locations) == 1
    assert sum(url.endswith("/tools") for url in locations) == 1
    assert sum(url.endswith(nonprofit) for url in locations) == 1
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for entry in root.findall("sm:url", namespace):
        if entry.findtext("sm:loc", namespaces=namespace).endswith((planner, "/tools", nonprofit, "/")):
            expected = (
                "2026-10-21"
                if entry.findtext("sm:loc", namespaces=namespace).endswith(planner)
                else "2026-10-23"
            )
            assert entry.findtext("sm:lastmod", namespaces=namespace) == expected


@pytest.mark.parametrize("name", ["content_review_planner", "for_nonprofits"])
def test_public_page_inputs_are_not_server_state_or_analytics(client, settings, name):
    settings.POSTHOG_API_KEY = "synthetic-project-key"
    settings.SITE_URL = "http://testserver"
    before = (Page.objects.count(), Sitemap.objects.count())
    marker = "private-synthetic-marker"
    path = reverse(name)
    response = client.get(path, {"pages": marker, "token": marker})
    assert response.status_code == 200
    assert marker not in response.content.decode()
    assert analytics_config(response) == {
        "api_key": "synthetic-project-key", "url": "http://testserver" + path,
        "signup_path": "/accounts/signup/",
    }
    assert marker not in json.dumps(analytics_config(response))
    assert client.post(path, {"pages": marker}).status_code == 405
    assert before == (Page.objects.count(), Sitemap.objects.count())
    assert client.get(path + "/private-synthetic-marker").status_code == 404


@pytest.mark.parametrize("status", [None, BlogPostStatus.DRAFT, BlogPostStatus.PUBLISHED])
def test_planner_workflow_handoff_only_links_published_comparison(client, status):
    path = "/blog/content-review-vs-change-monitoring"
    if status is not None:
        BlogPost.objects.create(
            title="Synthetic comparison",
            slug="content-review-vs-change-monitoring",
            content="Synthetic body",
            tags="",
            status=status,
        )
    html = client.get(reverse("content_review_planner")).content.decode()
    assert (f'href="{path}"' in html) == (status == BlogPostStatus.PUBLISHED)
    assert "Synthetic comparison" not in html
    assert "Synthetic body" not in html
    assert "calendar or task system" in html
    assert "cannot guarantee that a particular page appears before its deadline" in html
