"""Render production templates from repository content in an isolated in-memory DB.

Run only in the Docker test service; output contains public fixtures and assets,
never production rows. Serve build/blog-preview locally for visual review.
"""

import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["DJANGO_SETTINGS_MODULE"] = "staleaway.settings_test"
os.environ["ENVIRONMENT"] = "test"
os.environ["SITE_URL"] = "https://staleaway.com"
for variable in ("POSTHOG_API_KEY", "LOGFIRE_TOKEN", "SENTRY_DSN"):
    os.environ[variable] = ""

import django  # noqa: E402
from django.conf import settings  # noqa: E402

# Replace the test DB before any connection or app initialization can occur.
settings.DATABASES["default"]["NAME"] = ":memory:"
settings.STORAGES["staticfiles"]["BACKEND"] = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)
settings.ALLOWED_HOSTS = ["testserver", "localhost"]
django.setup()

from urllib.parse import urlparse  # noqa: E402

from django.contrib.sites.models import Site  # noqa: E402
from django.core.management import call_command  # noqa: E402
from django.test import Client  # noqa: E402

from core.blog_publishing import load_publications  # noqa: E402
from core.models import BlogPost  # noqa: E402

call_command("migrate", run_syncdb=True, verbosity=0)
# Fixture site matches the public canonical origin; never touches production.
Site.objects.update_or_create(
    pk=settings.SITE_ID,
    defaults={"domain": urlparse(settings.SITE_URL).netloc, "name": "Staleaway"},
)
# This previews the desired reviewed files, not production transition history.
# The database is in-memory and has no prior publication to compare against.
for desired, _previous_digest in load_publications(ROOT / "content" / "blog"):
    desired.save(force_insert=True)
output = ROOT / "build" / "blog-preview"
output.mkdir(parents=True, exist_ok=True)
shutil.copytree(ROOT / "frontend" / "build", output / "static", dirs_exist_ok=True)
client = Client()
paths = ["/", "/blog", "/tools", "/tools/content-review-planner", "/for/nonprofits", *[post.get_absolute_url() for post in BlogPost.objects.all()]]
for url in paths:
    response = client.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Preview failed: {url}: HTTP {response.status_code}")
    destination = output / url.lstrip("/") / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)
    if url == "/":
        (output / "home.html").write_bytes(response.content)
    elif url == "/blog":
        (output / "blog.html").write_bytes(response.content)
    elif url == "/blog/website-content-review-checklist":
        (output / "article.html").write_bytes(response.content)
sitemap = client.get("/sitemap.xml")
if sitemap.status_code != 200:
    raise RuntimeError("Preview sitemap failed")
(output / "sitemap.xml").write_bytes(sitemap.content)
print(f"Rendered {len(paths)} public previews in build/blog-preview")

# Exercise account setup templates with synthetic users, no network or real rows.
from unittest.mock import patch  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from allauth.account.models import EmailAddress  # noqa: E402
from core.models import Page, Sitemap  # noqa: E402

with patch('core.models.async_task'), patch('core.signals.async_task'), patch('core.tasks.async_task'):
    preview_user = get_user_model().objects.create_user(username='setup-preview', email='preview@example.com')
    EmailAddress.objects.create(user=preview_user, email=preview_user.email, primary=True, verified=True)
    client.force_login(preview_user)
    setup_cases = [('setup-first', client.get('/home')),
                   ('setup-first-error', client.post('/home', {'sitemap_url': 'not-a-url'}))]
    preview_sitemap = Sitemap.objects.create(profile=preview_user.profile, sitemap_url='https://example.com/sitemap.xml',
                                            pages_per_review=3, review_cadence='weekly')
    setup_cases.extend([('setup-existing', client.get('/home')),
                        ('setup-existing-error', client.post('/home', {'sitemap_url': 'not-a-url'}))])
    setup_cases.append(('setup-pages-empty', client.get(f'/sitemap/{preview_sitemap.pk}')))
    Page.objects.create(profile=preview_user.profile, sitemap=preview_sitemap, url='https://example.com/about')
    setup_cases.extend([('setup-pages-imported', client.get(f'/sitemap/{preview_sitemap.pk}')),
                        ('setup-settings', client.get('/settings'))])
    for name, response in setup_cases:
        if response.status_code != 200:
            raise RuntimeError(f'Setup preview failed: {name}: HTTP {response.status_code}')
        (output / f'{name}.html').write_bytes(response.content)
print(f'Rendered {len(setup_cases)} synthetic setup states; no production data or sends')
