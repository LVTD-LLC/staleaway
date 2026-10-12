"""Activation means account creation and backend acceptance, never email delivery."""
from unittest.mock import Mock

import pytest
from allauth.account.signals import user_signed_up
from django.db import transaction
from django.test import RequestFactory
from django.urls import reverse

from core.models import EmailSent, Page, Sitemap
from core.tasks import queue_activation_event, send_page_email_to_profile, track_event

pytestmark = pytest.mark.django_db


@pytest.fixture
def capture(monkeypatch, settings):
    settings.POSTHOG_API_KEY = "synthetic-project-key"
    settings.SITE_URL = "https://staleaway.com"
    capture = Mock(return_value=(True, {}))
    monkeypatch.setattr("core.tasks.posthog.capture", capture)
    return capture


@pytest.fixture
def queued(monkeypatch, settings):
    settings.POSTHOG_API_KEY = "synthetic-project-key"
    queued = Mock()
    monkeypatch.setattr("core.tasks.async_task", queued)
    return queued


def test_real_signup_route_queues_only_after_successful_commit(
    client, queued, settings, django_capture_on_commit_callbacks, django_user_model
):
    settings.ACCOUNT_EMAIL_VERIFICATION = "none"
    client.cookies["private-cookie"] = "private-marker"
    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(reverse("account_signup"), {
            "username": "new-owner", "email": "private-marker@example.invalid",
            "password1": "a-long-unusual-test-password-782!",
            "password2": "a-long-unusual-test-password-782!",
        })
        queued.assert_not_called()
    assert response.status_code == 302
    user = django_user_model.objects.get(username="new-owner")
    queued.assert_called_once_with(
        "core.tasks.track_event", profile_id=user.profile.pk,
        event_name="user_signed_up", properties={}, email_sent_id=None,
        group="Track Event",
    )
    assert "private-marker" not in str(queued.call_args)


def test_invalid_signup_is_not_a_success(client, queued, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        assert client.post(reverse("account_signup"), {}).status_code == 200
    queued.assert_not_called()


def test_social_signup_uses_same_signal_without_copying_provider_data(
    user, queued, django_capture_on_commit_callbacks
):
    sociallogin = Mock(user=user)
    with django_capture_on_commit_callbacks(execute=True):
        user_signed_up.send(
            sender=type(user), request=RequestFactory().post('/accounts/signup/'),
            user=user, sociallogin=sociallogin,
        )
    queued.assert_called_once()
    assert queued.call_args.kwargs['event_name'] == 'user_signed_up'
    assert queued.call_args.kwargs['properties'] == {}
    assert user.email not in str(queued.call_args)


def test_rolled_back_signup_never_queues(profile, queued, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        with pytest.raises(ValueError):
            with transaction.atomic():
                queue_activation_event(profile.pk, "user_signed_up")
                raise ValueError("rollback")
    queued.assert_not_called()


def test_queue_failure_does_not_fail_signup(
    client, queued, settings, django_capture_on_commit_callbacks, monkeypatch
):
    settings.ACCOUNT_EMAIL_VERIFICATION = "none"
    queued.side_effect = RuntimeError("private-provider-detail")
    log = Mock()
    monkeypatch.setattr('core.tasks.logger', log)
    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(reverse('account_signup'), {
            'username': 'queue-down', 'email': 'queue@example.invalid',
            'password1': 'another-unusual-password-823!', 'password2': 'another-unusual-password-823!',
        })
    assert response.status_code == 302
    log.warning.assert_called_once_with('Activation analytics queue unavailable')


def test_signup_retry_uses_same_pseudonym_timestamp_and_uuid(profile, capture):
    track_event(profile.pk, 'user_signed_up', {'email': profile.user.email})
    first = capture.call_args
    track_event(profile.pk, 'user_signed_up', {'token': 'private-marker'})
    assert capture.call_args == first
    assert first.kwargs['timestamp'] == profile.user.date_joined
    assert first.kwargs['uuid'].version == 5
    assert profile.user.email not in str(first)
    assert 'private-marker' not in str(first)


def test_first_reminder_requires_correct_account_and_first_record(profile, user, capture, django_user_model):
    other = django_user_model.objects.create_user(username='other-analytics', email='other@example.invalid')
    other_send = EmailSent.objects.create(profile=other.profile)
    track_event(profile.pk, 'first_review_reminder_accepted', {}, email_sent_id=other_send.pk)
    capture.assert_not_called()
    first = EmailSent.objects.create(profile=profile)
    later = EmailSent.objects.create(profile=profile)
    track_event(profile.pk, 'first_review_reminder_accepted', {}, email_sent_id=later.pk)
    capture.assert_not_called()
    track_event(profile.pk, 'first_review_reminder_accepted', {'private_url': 'private-marker'}, email_sent_id=first.pk)
    original = capture.call_args
    assert original.kwargs['timestamp'] == first.created_at
    assert original.kwargs['properties']['measurement_version'] == 'activation-v1'
    assert set(original.kwargs['properties']) == {
        '$host', '$process_person_profile', '$geoip_disable', 'measurement_version', 'source'
    }
    assert 'private-marker' not in str(original)
    track_event(profile.pk, 'first_review_reminder_accepted', {}, email_sent_id=first.pk)
    assert capture.call_args == original
    track_event(profile.pk, 'user_signed_up', {})
    assert capture.call_args.args == original.args
    assert capture.call_args.kwargs['uuid'] != original.kwargs['uuid']


@pytest.mark.parametrize('missing', ['key', 'profile'])
def test_missing_configuration_or_profile_does_not_capture(profile, capture, settings, missing):
    if missing == 'key':
        settings.POSTHOG_API_KEY = ''
    else:
        profile.delete()
    track_event(profile.pk or 999999, 'user_signed_up', {})
    capture.assert_not_called()


def test_sdk_queue_rejection_is_not_reported_as_delivered(profile, capture):
    capture.return_value = (False, {})
    with pytest.raises(RuntimeError, match='enqueue failed'):
        track_event(profile.pk, 'user_signed_up', {})


@pytest.fixture
def reminder(profile, monkeypatch):
    sitemap = Sitemap.objects.create(profile=profile, sitemap_url='https://example.invalid/sitemap.xml')
    Page.objects.create(profile=profile, sitemap=sitemap, url='https://example.invalid/private-marker')
    monkeypatch.setattr('core.tasks.fetch_page_metadata', lambda url: {})
    monkeypatch.setattr('django.template.loader.render_to_string', lambda *args, **kwargs: '<p>Review</p>')
    send = Mock(return_value=1)
    monkeypatch.setattr('django.core.mail.EmailMultiAlternatives.send', send)
    return send


def test_accepted_reminder_queues_after_send_record_commit(
    profile, reminder, queued, django_capture_on_commit_callbacks
):
    with django_capture_on_commit_callbacks(execute=True):
        assert send_page_email_to_profile(profile.pk).startswith('Successfully sent')
        queued.assert_not_called()
    sent = EmailSent.objects.get(profile=profile)
    queued.assert_called_once_with(
        'core.tasks.track_event', profile_id=profile.pk,
        event_name='first_review_reminder_accepted', properties={}, email_sent_id=sent.pk,
        group='Track Event',
    )
    assert 'private-marker' not in str(queued.call_args)


@pytest.mark.parametrize('outcome', [0, RuntimeError('provider failed')])
def test_unaccepted_email_creates_no_send_record_or_activation(
    profile, reminder, queued, django_capture_on_commit_callbacks, outcome
):
    if isinstance(outcome, Exception):
        reminder.side_effect = outcome
    else:
        reminder.return_value = outcome
    with django_capture_on_commit_callbacks(execute=True):
        assert not send_page_email_to_profile(profile.pk).startswith('Successfully sent')
    assert not EmailSent.objects.filter(profile=profile).exists()
    queued.assert_not_called()


def test_analytics_outage_does_not_turn_accepted_reminder_into_failure(
    profile, reminder, queued, django_capture_on_commit_callbacks
):
    queued.side_effect = RuntimeError('queue unavailable')
    with django_capture_on_commit_callbacks(execute=True):
        assert send_page_email_to_profile(profile.pk).startswith('Successfully sent')
    assert EmailSent.objects.filter(profile=profile).count() == 1
    reminder.assert_called_once()
