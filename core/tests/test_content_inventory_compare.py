import json
import re
from pathlib import Path
from xml.etree import ElementTree

import pytest
from django.urls import reverse

from core.choices import BlogPostStatus
from core.models import BlogPost, Page, Sitemap
from core.tests.test_analytics_privacy import analytics_config
from core.tests.test_public_seo import schemas

pytestmark = pytest.mark.django_db


def test_inventory_tool_is_public_indexable_and_server_rendered(client, settings):
    settings.SITE_URL = "https://canonical.example"
    path = reverse("content_inventory_compare")
    response = client.get(path)
    assert response.status_code == 200
    html = response.content.decode()
    assert html.count('<link rel="canonical"') == 1
    assert f'<link rel="canonical" href="https://canonical.example{path}"' in html
    assert "noindex" not in html
    assert len(re.search(r"<title>(.*?)</title>", html).group(1)) <= 60
    assert len(re.search(r'<meta name="description" content="(.*?)"', html).group(1)) <= 155
    assert html.count("<h1>") == 1
    assert "Content inventory comparison tool" in html
    assert "Matching preserves what you pasted" in html
    assert 'data-controller="content-inventory-compare"' in html
    assert '<fieldset disabled data-content-inventory-compare-target="fields">' in html
    assert 'data-content-inventory-compare-target="result" hidden' in html
    assert "No comparison has run." in html
    assert '<a href="#manual-inventory-worksheet">' in html
    assert "<noscript>" in html
    assert 'type="file"' not in html
    assert '<textarea' in html
    for key in ["inventory", "sitemap", "imported"]:
        assert f'for="inventory-{key}"' in html
        assert f'aria-describedby="inventory-{key}-hint inventory-limits inventory-{key}-error"' in html
    data = schemas(response)
    assert data[0]["@type"] == "WebApplication"
    assert data[0]["url"] == settings.SITE_URL + path
    assert data[0]["offers"] == {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    assert data[0]["dateModified"] == "2026-11-01"
    assert data[0]["isAccessibleForFree"] is True
    assert data[1]["@type"] == "BreadcrumbList"
    assert data[1]["itemListElement"][-1]["item"] == settings.SITE_URL + path


def test_inventory_discovery_and_precise_sitemap_dates(client):
    path = reverse("content_inventory_compare")
    for source in ["/", "/tools"]:
        html = client.get(source).content.decode()
        assert f'href="{path}"' in html
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    root = ElementTree.fromstring(response.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries = {
        row.findtext("sm:loc", namespaces=ns): row.findtext("sm:lastmod", namespaces=ns)
        for row in root.findall("sm:url", ns)
    }
    assert sum(url.endswith(path) for url in entries) == 1
    for suffix in [path, "/tools", "/"]:
        expected = "2026-11-01" if suffix == path else "2026-11-06"
        assert next(value for url, value in entries.items() if url.endswith(suffix)) == expected
    assert next(value for url, value in entries.items() if url.endswith("/tools/content-review-planner")) == "2026-11-05"


def test_inventory_never_receives_or_persists_comparison_values(client, settings):
    path = reverse("content_inventory_compare")
    settings.POSTHOG_API_KEY = "synthetic-project-key"
    settings.SITE_URL = "http://testserver"
    before = (Page.objects.count(), Sitemap.objects.count())
    marker = "synthetic-private-marker"
    response = client.get(path, {"inventory": marker, "token": marker})
    assert response.status_code == 200
    assert marker not in response.content.decode()
    assert analytics_config(response) == {
        "api_key": "synthetic-project-key", "url": "http://testserver" + path,
        "signup_path": "/accounts/signup/",
    }
    assert marker not in json.dumps(analytics_config(response))
    assert client.post(path, {"inventory": marker}).status_code == 405
    assert client.get(path + "/" + marker).status_code == 404
    assert before == (Page.objects.count(), Sitemap.objects.count())
    source = Path("frontend/src/controllers/content_inventory_compare_controller.js").read_text()
    logic = Path("frontend/src/tools/content_inventory_compare.js").read_text()
    for forbidden in ["innerHTML", "fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "location."]:
        assert forbidden not in source + logic


@pytest.mark.parametrize("status", [None, BlogPostStatus.DRAFT, BlogPostStatus.PUBLISHED])
@pytest.mark.parametrize("name", ["content_inventory_compare", "for_documentation", "for_wordpress"])
def test_inventory_links_only_published_guides(client, status, name):
    slugs = ["find-your-website-sitemap", "website-content-review-checklist"]
    if status is not None:
        for slug in slugs:
            BlogPost.objects.create(title="Synthetic private title", slug=slug, content="Synthetic private body", tags="", status=status)
    html = client.get(reverse(name)).content.decode()
    for slug in slugs:
        assert (f'href="/blog/{slug}' in html) == (status == BlogPostStatus.PUBLISHED)
    assert "Synthetic private title" not in html
    assert "Synthetic private body" not in html
    assert 'href="/tools/content-review-planner"' in html
