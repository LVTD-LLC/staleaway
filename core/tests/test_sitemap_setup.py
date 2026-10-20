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


@pytest.mark.parametrize('has_pages', [False, True])
def test_post_import_handoff_reaches_owned_settings(auth_client, profile, django_user_model, has_pages):
    from allauth.account.models import EmailAddress
    from core.models import Page

    EmailAddress.objects.create(user=profile.user, email=profile.user.email, primary=True, verified=True)
    sitemap = Sitemap.objects.create(profile=profile, sitemap_url='https://example.com/sitemap.xml',
                                    pages_per_review=3, review_cadence='weekly')
    if has_pages:
        Page.objects.create(profile=profile, sitemap=sitemap, url='https://example.com/about')
    other = django_user_model.objects.create_user(username='other-handoff', email='other@example.com')
    private = Sitemap.objects.create(profile=other.profile, sitemap_url='https://private.example/sitemap.xml')
    target = f'/settings#sitemap-settings-{sitemap.pk}'
    for path in ['/home', f'/sitemap/{sitemap.pk}']:
        response = auth_client.get(path)
        assert response.status_code == 200
        html = response.content.decode()
        assert f'href="{target}"' in html
        assert 'Saved cadence: Weekly · Up to 3 pages per review email' in html
        assert 'href="/settings#reminder-settings"' in html
        assert 'public-analytics-config' not in html
        assert private.sitemap_url not in html
        assert f'href="/settings#sitemap-settings-{private.pk}"' not in html
        if path.startswith('/sitemap/'):
            assert ('No imported pages to show yet' in html) == (not has_pages)
            assert ('Check for imported pages' in html) == (not has_pages)
    settings_response = auth_client.get('/settings')
    assert settings_response.status_code == 200
    settings_html = settings_response.content.decode()
    assert f'id="sitemap-settings-{sitemap.pk}"' in settings_html
    assert 'id="reminder-settings"' in settings_html
    assert f'id="sitemap-settings-{private.pk}"' not in settings_html
    assert auth_client.get(f'/sitemap/{private.pk}').status_code == 404
