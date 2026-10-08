import re
from xml.etree import ElementTree

import pytest
from django.contrib.sites.models import Site
from django.urls import reverse

from core.choices import BlogPostStatus
from core.models import BlogPost
from staleaway.indexnow_views import KEY


def test_public_ownership_and_revision(client, settings, tmp_path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "deployment-revision.txt").write_text("abc123")
    response = client.get(reverse("indexnow_key"))
    assert response.status_code == 200
    assert response.content.decode().strip() == KEY
    assert re.fullmatch(r"[a-zA-Z0-9-]{8,128}", KEY)
    assert response["Content-Type"].startswith("text/plain")
    assert "no-store" in response["Cache-Control"]
    assert client.post(reverse("indexnow_key")).status_code == 405
    assert client.get(reverse("deployment_revision")).content == b"abc123\n"


@pytest.mark.django_db
def test_sitemap_public_pages_and_full_blog_modification_timestamp(client, settings):
    Site.objects.update_or_create(pk=settings.SITE_ID, defaults={"domain": "testserver"})
    Site.objects.clear_cache()
    published = BlogPost.objects.create(
        title="Public",
        slug="public",
        content="Public content",
        tags="",
        status=BlogPostStatus.PUBLISHED,
    )
    BlogPost.objects.create(title="Draft", slug="draft", content="Private draft", tags="")
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    root = ElementTree.fromstring(response.content)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {node.findtext("s:loc", namespaces=ns): node for node in root}
    paths = [url.removeprefix("https://testserver") for url in urls]
    assert sorted(paths) == ["/", "/blog", "/blog/public", "/uses"]
    stamp = urls["https://testserver/blog/public"].findtext("s:lastmod", namespaces=ns)
    assert stamp == published.updated_at.isoformat()
