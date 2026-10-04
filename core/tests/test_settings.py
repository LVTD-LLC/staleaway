import os
import subprocess
import sys


def get_default_from_email(env):
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from django.conf import settings; "
                "print(settings.DEFAULT_FROM_EMAIL)"
            ),
        ],
        check=True,
        capture_output=True,
        env=env,
        text=True,
    )
    return result.stdout.strip()


def test_default_from_email_uses_staleaway_sender_when_env_is_unset():
    env = os.environ.copy()
    env["DJANGO_SETTINGS_MODULE"] = "staleaway.settings_test"
    env.pop("DEFAULT_FROM_EMAIL", None)

    assert get_default_from_email(env) == "Rasul from Staleaway <rasul@staleaway.com>"


def test_default_from_email_can_be_overridden_by_env():
    env = os.environ.copy()
    env["DJANGO_SETTINGS_MODULE"] = "staleaway.settings_test"
    env["DEFAULT_FROM_EMAIL"] = "Staleaway Support <support@example.com>"

    assert get_default_from_email(env) == "Staleaway Support <support@example.com>"
