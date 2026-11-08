import json
import re

import pytest

from core.choices import BlogPostStatus
from core.models import BlogPost

pytestmark = pytest.mark.django_db


def schemas(response):
    return [
        json.loads(value)
        for value in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            response.content.decode(),
            re.S,
        )
    ]


def test_public_discovery_uses_configured_origin(client, settings):
    settings.SITE_URL = "https://canonical-site.example/"
    for path in ("/", "/blog", "/uses", "/for/nonprofits", "/for/documentation", "/for/wordpress"):
        response = client.get(path)
        assert response.status_code == 200
        html = response.content.decode()
        suffix = path if path != "/" else "/"
        assert f'<link rel="canonical" href="https://canonical-site.example{suffix}"' in html
        assert 'href="/blog"' in html
        assert 'href="/uses"' in html
        assert "noindex" not in html
        data = schemas(response)
        assert data
        if path.startswith("/for/"):
            assert len(re.findall(r'<link rel="canonical"', html)) == 1
            assert data[0]["@type"] == "WebPage"
            assert data[0]["url"] == "https://canonical-site.example" + path
            published, modified = {
                "/for/nonprofits": ("2026-10-23", "2026-11-02"),
                "/for/documentation": ("2026-11-06", "2026-11-06"),
                "/for/wordpress": ("2026-11-08", "2026-11-08"),
            }[path]
            assert data[0]["datePublished"] == published
            assert data[0]["dateModified"] == modified
            assert len(re.findall(r"<h1[ >]", html)) == 1
            assert len(re.search(r"<title>(.*?)</title>", html).group(1)) <= 60
            assert len(re.search(r'<meta name="description" content="(.*?)"', html).group(1)) <= 155
            breadcrumbs = next(item for item in data if item["@type"] == "BreadcrumbList")
            assert breadcrumbs["itemListElement"][-1]["item"] == data[0]["url"]
    home = client.get("/").content.decode()
    assert "<title>Free Website Content Review Email Reminders | Staleaway</title>" in home
    assert "Staleaway emails content review reminders, a few pages at a time." in home
    assert schemas(client.get("/"))[0]["url"] == "https://canonical-site.example/"
    robots = client.get("/robots.txt")
    assert robots.status_code == 200
    assert robots["Content-Type"].startswith("text/plain")
    assert "Sitemap: https://canonical-site.example/sitemap.xml" in robots.content.decode()
    assert "Disallow: /\n" not in robots.content.decode()


def test_only_published_blog_posts_are_public(client):
    draft = BlogPost.objects.create(
        title="Private draft", slug="private-draft", content="Private body", tags=""
    )
    published = BlogPost.objects.create(
        title="Public post",
        slug="public-post",
        content="Public body",
        tags="",
        status=BlogPostStatus.PUBLISHED,
    )
    listing = client.get("/blog")
    assert listing.status_code == 200
    assert "Public post" in listing.content.decode()
    assert "Private draft" not in listing.content.decode()
    assert client.get(draft.get_absolute_url()).status_code == 404
    assert client.get(published.get_absolute_url()).status_code == 200
    assert client.get("/blog/does-not-exist").status_code == 404


@pytest.mark.parametrize("image", ["", "blog_post_images/example.jpg"])
def test_blog_schema_round_trips_text_and_optional_image(client, settings, image):
    settings.SITE_URL = "https://canonical-site.example/"
    title = 'Review "this" & that </script> \\ end'
    description = "Line one\nLine two & <three>"
    post = BlogPost.objects.create(
        title=title,
        slug="schema-check",
        description=description,
        content='## A heading\nA "quote" and a backslash \\.',
        tags="",
        image=image,
        status=BlogPostStatus.PUBLISHED,
    )
    response = client.get(post.get_absolute_url())
    assert response.status_code == 200
    data = schemas(response)[0]
    assert data["headline"] == title
    assert data["description"] == description
    assert data["url"] == "https://canonical-site.example/blog/schema-check"
    assert data["mainEntityOfPage"]["@id"] == data["url"]
    assert data["dateModified"] == post.updated_at.isoformat()
    assert bool(data.get("image")) == bool(image)
    assert "articleBody" not in data
    assert (
        '<link rel="canonical" href="https://canonical-site.example/blog/schema-check"'
        in response.content.decode()
    )
