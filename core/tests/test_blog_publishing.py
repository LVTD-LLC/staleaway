import hashlib
import json
from io import StringIO
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.core.management import call_command
from django.core.management.base import CommandError

from core.blog_publishing import (
    load_publications,
    publication_digest,
    publish_repository_posts,
    repository_post_uuid,
)
from core.choices import BlogPostStatus
from core.models import BlogPost
from core.tests.test_public_seo import schemas

pytestmark = pytest.mark.django_db


def write_publication(
    directory,
    slug="website-content-review-checklist",
    *,
    previous=None,
    content="## Check the page\n\nReview facts and links.\n",
):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{slug}.md").write_text(content)
    manifest = {
        "schema_version": 1,
        "slug": slug,
        "title": "Website content review checklist",
        "description": "A practical checklist for recurring page reviews.",
        "tags": "content review, website maintenance",
        "author": "Staleaway",
        "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
        "expected_previous_sha256": previous,
    }
    (directory / f"{slug}.json").write_text(json.dumps(manifest))
    return manifest


def test_publish_is_idempotent_and_dry_run_does_not_write(tmp_path):
    write_publication(tmp_path)
    assert publish_repository_posts(tmp_path, dry_run=True)[0][1] == "create"
    assert not BlogPost.objects.exists()
    assert publish_repository_posts(tmp_path)[0][1] == "create"
    post = BlogPost.objects.get()
    timestamps = (post.created_at, post.updated_at)
    assert post.status == BlogPostStatus.PUBLISHED
    assert post.uuid == repository_post_uuid(post.slug)
    assert publish_repository_posts(tmp_path)[0][1] == "unchanged"
    post.refresh_from_db()
    assert (post.created_at, post.updated_at) == timestamps
    assert BlogPost.objects.count() == 1


@pytest.mark.parametrize("status", [BlogPostStatus.DRAFT, BlogPostStatus.PUBLISHED])
def test_existing_unmanaged_content_is_never_claimed(tmp_path, status):
    manifest = write_publication(tmp_path)
    post = BlogPost.objects.create(
        slug=manifest["slug"],
        title="Existing",
        content="Private editorial body",
        tags="",
        status=status,
    )
    with pytest.raises(CommandError, match="collision"):
        publish_repository_posts(tmp_path)
    post.refresh_from_db()
    assert post.content == "Private editorial body"
    assert post.status == status
    assert BlogPost.objects.count() == 1


def test_updates_require_exact_previous_record_and_preserve_created_date(tmp_path):
    write_publication(tmp_path)
    publish_repository_posts(tmp_path)
    post = BlogPost.objects.get()
    previous = publication_digest(post)
    created = post.created_at
    write_publication(tmp_path, content="## Revised checklist\n")
    with pytest.raises(CommandError, match="differs"):
        publish_repository_posts(tmp_path)
    write_publication(tmp_path, previous=previous, content="## Revised checklist\n")
    assert publish_repository_posts(tmp_path, dry_run=True)[0][1] == "update"
    post.refresh_from_db()
    assert publication_digest(post) == previous
    assert publish_repository_posts(tmp_path)[0][1] == "update"
    post.refresh_from_db()
    assert post.content == "## Revised checklist\n"
    assert post.created_at == created
    assert publish_repository_posts(tmp_path)[0][1] == "unchanged"


@pytest.mark.parametrize(
    "field,value",
    [
        ("title", "Editorial title"),
        ("image", "blog_post_images/manual.jpg"),
        ("status", BlogPostStatus.DRAFT),
    ],
)
def test_editorial_changes_and_withdrawals_stop_updates(tmp_path, field, value):
    write_publication(tmp_path)
    publish_repository_posts(tmp_path)
    post = BlogPost.objects.get()
    previous = publication_digest(post)
    setattr(post, field, value)
    post.save()
    write_publication(tmp_path, previous=previous, content="New approved body")
    with pytest.raises(CommandError):
        publish_repository_posts(tmp_path)
    post.refresh_from_db()
    assert str(getattr(post, field)) == value
    assert post.content != "New approved body"
    if field == "status":
        write_publication(tmp_path, previous=publication_digest(post), content="New approved body")
        with pytest.raises(CommandError, match="refusing to republish"):
            publish_repository_posts(tmp_path)


def test_duplicate_slug_or_moved_repository_uuid_stops_publication(tmp_path):
    manifest = write_publication(tmp_path)
    publish_repository_posts(tmp_path)
    post = BlogPost.objects.get()
    post.slug = "moved-by-editor"
    post.save()
    with pytest.raises(CommandError, match="collision"):
        publish_repository_posts(tmp_path)
    post.slug = manifest["slug"]
    post.save()
    BlogPost.objects.create(slug=post.slug, title="Another draft", content="Private", tags="")
    with pytest.raises(CommandError, match="collision"):
        publish_repository_posts(tmp_path)


def test_invalid_markdown_digest_and_missing_previous_fail_closed(tmp_path):
    write_publication(tmp_path)
    (tmp_path / "website-content-review-checklist.md").write_text("Unapproved edit")
    with pytest.raises(CommandError, match="digest"):
        publish_repository_posts(tmp_path)
    write_publication(tmp_path, previous="0" * 64)
    with pytest.raises(CommandError, match="missing"):
        publish_repository_posts(tmp_path)
    assert not BlogPost.objects.exists()


def test_all_publications_roll_back_on_later_collision(tmp_path):
    write_publication(tmp_path, "a-first")
    write_publication(tmp_path, "z-last")
    BlogPost.objects.create(slug="z-last", title="Keep", content="Private", tags="")
    with pytest.raises(CommandError):
        publish_repository_posts(tmp_path)
    assert not BlogPost.objects.filter(slug="a-first").exists()


def test_management_command_and_public_discovery(tmp_path, settings, client):
    settings.BASE_DIR = tmp_path
    slugs = ("website-content-review-checklist", "find-your-website-sitemap")
    for slug in slugs:
        write_publication(tmp_path / "content" / "blog", slug)
    output = StringIO()
    call_command("publish_repository_blog", stdout=output)
    assert "publication_sha256=" in output.getvalue()
    assert BlogPost.objects.count() == len(slugs)
    discovery_pages = ("/", "/blog", "/sitemap.xml")
    for post in BlogPost.objects.all():
        for path in discovery_pages:
            assert post.get_absolute_url() in client.get(path).content.decode()
        response = client.get(post.get_absolute_url())
        html = response.content.decode()
        assert response.status_code == 200
        assert "By Staleaway" in html
        assert '<meta name="twitter:creator"' not in html
        data = {item["@type"]: item for item in schemas(response)}
        assert data["BlogPosting"]["author"]["@type"] == "Organization"
        assert data["BlogPosting"]["author"]["name"] == "Staleaway"
        assert data["BreadcrumbList"]["itemListElement"][-1]["name"] == post.title
        assert len(data["HowTo"]["step"]) == 5
        assert data["BlogPosting"]["datePublished"] == post.created_at.isoformat()
        if post.slug == "find-your-website-sitemap":
            assert data["HowTo"]["step"][0]["name"] == "Find the sitemap address"
            assert data["HowTo"]["step"][-1]["name"] == "Import and verify listed pages"
            assert len(data["FAQPage"]["mainEntity"]) == 3
        else:
            assert "FAQPage" not in data
    for post in BlogPost.objects.all():
        post.status = BlogPostStatus.DRAFT
        post.save()
        for path in discovery_pages:
            assert post.get_absolute_url() not in client.get(path).content.decode()
        assert client.get(post.get_absolute_url()).status_code == 404


@pytest.mark.parametrize("slug", ["existing-post", "find-your-website-sitemap"])
def test_existing_author_attribution_is_unchanged(client, slug):
    post = BlogPost.objects.create(
        slug=slug,
        title="Existing",
        content="Body",
        tags="",
        status=BlogPostStatus.PUBLISHED,
    )
    data = {item["@type"]: item for item in schemas(client.get(post.get_absolute_url()))}
    assert data["BlogPosting"]["author"]["name"] == "Rasul Kireev"
    assert "HowTo" not in data
    assert "FAQPage" not in data


def test_repository_manifests_publish_and_render(client, settings):
    # Exercise the actual reviewed artifact, not just synthetic fixtures.
    source = Path(__file__).resolve().parents[2] / "content" / "blog"
    # Desired-state rendering is independent of production transition history.
    publications = load_publications(source)
    assert {post.slug for post, _ in publications} >= {
        "website-content-review-checklist", "find-your-website-sitemap"
    }
    for desired, _previous_digest in publications:
        desired.save(force_insert=True)
    for post in BlogPost.objects.all():
        response = client.get(post.get_absolute_url())
        assert response.status_code == 200
        html = response.content.decode()
        data = {item["@type"]: item for item in schemas(response)}
        assert data["BlogPosting"]["url"].endswith(post.get_absolute_url())
        assert "By Staleaway" in html
        assert f'<link rel="canonical" href="{data["BlogPosting"]["url"]}"' in html
        assert post.get_absolute_url() in client.get("/blog").content.decode()
        assert post.get_absolute_url() in client.get("/sitemap.xml").content.decode()
        if post.slug == "find-your-website-sitemap":
            assert "worksheet" in html.lower()
            assert 'href="/accounts/signup/"' in html
            assert 'href="/blog/website-content-review-checklist"' in html
            assert len(data["HowTo"]["step"]) == 5
            # Structured answers must match the visible article, not only valid JSON.
            visible_article = BeautifulSoup(html, "html.parser").select_one("article").get_text(
                " ", strip=True
            )
            for question in data["FAQPage"]["mainEntity"]:
                assert question["name"] in visible_article
                assert question["acceptedAnswer"]["text"] in visible_article


@pytest.mark.parametrize("directory_exists", [False, True])
def test_missing_or_empty_manifest_directory_is_non_destructive_noop(
    tmp_path, settings, directory_exists
):
    settings.BASE_DIR = tmp_path
    directory = tmp_path / "content" / "blog"
    if directory_exists:
        directory.mkdir(parents=True)
    post = BlogPost.objects.create(
        slug="unrelated",
        title="Keep",
        content="Existing editorial content",
        tags="",
        status=BlogPostStatus.PUBLISHED,
    )
    before = (publication_digest(post), post.created_at, post.updated_at)
    output = StringIO()
    call_command("publish_repository_blog", stdout=output)
    assert "No repository blog manifests; no rows changed." in output.getvalue()
    assert publish_repository_posts(directory, dry_run=True) == []
    post.refresh_from_db()
    assert (publication_digest(post), post.created_at, post.updated_at) == before
    assert BlogPost.objects.count() == 1


def test_present_malformed_manifest_is_not_treated_as_empty(tmp_path):
    (tmp_path / "broken.json").write_text("{invalid json")
    with pytest.raises(CommandError, match="Invalid publication manifest"):
        publish_repository_posts(tmp_path)


def test_revision_manifest_can_render_as_isolated_desired_fixture(tmp_path, client):
    write_publication(tmp_path, previous="0" * 64)
    # Production still refuses a missing predecessor; only test fixtures bypass
    # that transition check after validating the manifest and Markdown digest.
    with pytest.raises(CommandError, match="missing"):
        publish_repository_posts(tmp_path)
    for desired, _previous_digest in load_publications(tmp_path):
        desired.save(force_insert=True)
    post = BlogPost.objects.get()
    response = client.get(post.get_absolute_url())
    assert response.status_code == 200
    assert "By Staleaway" in response.content.decode()
    assert schemas(response)
