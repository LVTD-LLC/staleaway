import re

import pytest

from core.choices import BlogPostStatus
from core.models import BlogPost, Sitemap

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('existing', [False, True])
@pytest.mark.parametrize('status', [None, BlogPostStatus.DRAFT, BlogPostStatus.PUBLISHED])
def test_setup_help_only_links_published_guide(auth_client, profile, existing, status):
    if existing:
        Sitemap.objects.create(profile=profile, sitemap_url='https://example.com/sitemap.xml')
    if status is not None:
        BlogPost.objects.create(title='Find your sitemap', slug='find-your-website-sitemap',
                                content='Public fixture', tags='', status=status)
    response = auth_client.get('/home')
    assert response.status_code == 200
    html = response.content.decode()
    assert ('href="/blog/find-your-website-sitemap"' in html) == (status == BlogPostStatus.PUBLISHED)
    assert html.count('id="sitemap-url-help"') == 1
    assert 'aria-describedby="sitemap-url-help sitemap-url-errors"' in html
    assert 'Saving a URL does not confirm that its pages imported.' in html
    if status == BlogPostStatus.PUBLISHED:
        assert 'target="_blank" rel="noopener noreferrer"' in html
    assert 'public-analytics-config' not in html


@pytest.mark.parametrize('existing', [False, True])
@pytest.mark.parametrize('value', ['', 'not-a-url'])
def test_invalid_submission_stays_visible_and_preserves_input(auth_client, profile, existing, value):
    if existing:
        Sitemap.objects.create(profile=profile, sitemap_url='https://example.com/sitemap.xml')
    response = auth_client.post('/home', {'sitemap_url': value})
    assert response.status_code == 200
    html = response.content.decode()
    assert 'data-sitemap-errors-value="true"' in html
    assert 'aria-invalid="true"' in html
    assert response.context['form']['sitemap_url'].value() == value
    assert Sitemap.objects.filter(profile=profile).count() == int(existing)
    if existing:
        container = re.search(r'<div class="([^"]*)" data-sitemap-target="formContainer">', html)
        assert container and 'hidden' not in container.group(1).split()
        assert re.search(r'data-sitemap-target="toggleButton"[^>]*>\s*Cancel\s*</button>', html)
    else:
        assert 'data-sitemap-target="onboardingModal"' in html


def test_setup_success_is_saved_not_import_verified_and_scoped(auth_client, profile, django_user_model):
    other = django_user_model.objects.create_user(username='other-setup', email='other@example.com')
    Sitemap.objects.create(profile=other.profile, sitemap_url='https://other.example/private.xml')
    response = auth_client.post('/home', {'sitemap_url': 'https://example.com/sitemap.xml'}, follow=True)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'Sitemap saved. Import runs in the background;' in html
    assert 'https://other.example/private.xml' not in html
    assert Sitemap.objects.get(profile=profile).import_status == 'pending'
    container = re.search(r'<div class="([^"]*)" data-sitemap-target="formContainer">', html)
    assert 'hidden' in container.group(1).split()
