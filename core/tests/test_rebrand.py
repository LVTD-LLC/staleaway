import json
import os
import subprocess
import sys

import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from staleaway.middleware import CanonicalHostMiddleware


def test_upgrade_keeps_storage_and_queue():
    env = os.environ.copy()
    for key in ["AWS_S3_BUCKET_NAME", "Q_CLUSTER_NAME"]:
        env.pop(key, None)
    env.update(
        DJANGO_SETTINGS_MODULE="staleaway.settings_test",
        ENVIRONMENT="prod",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import json; from staleaway import settings as s; "
            "print(json.dumps([s.folder_name, s.Q_CLUSTER['name']]))",
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout) == ["cleanapp-prod", "cleanapp-q"]
    env.update(
        AWS_S3_BUCKET_NAME="existing-media",
        Q_CLUSTER_NAME="existing-queue",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import json; from staleaway import settings as s; "
            "print(json.dumps([s.folder_name, s.Q_CLUSTER['name']]))",
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout) == ["existing-media", "existing-queue"]


@pytest.mark.parametrize("method", ["get", "head"])
def test_legacy_links_preserve_path_and_query(settings, method):
    settings.SITE_URL = "https://staleaway.com"
    settings.LEGACY_HOSTS = ["pagefresh.lvtd.dev"]
    settings.ALLOWED_HOSTS = settings.LEGACY_HOSTS
    request = getattr(RequestFactory(), method)(
        "/review-page/123/?token=example", HTTP_HOST="pagefresh.lvtd.dev"
    )
    response = CanonicalHostMiddleware(lambda request: HttpResponse("ok"))(request)
    assert response.status_code == 301
    assert response["Location"] == "https://staleaway.com/review-page/123/?token=example"


def test_legacy_api_post_is_not_redirected(settings):
    settings.LEGACY_HOSTS = ["pagefresh.lvtd.dev"]
    request = RequestFactory().post(
        "/api/submit-feedback",
        data=b'{"type":"test"}',
        content_type="application/json",
        HTTP_HOST="pagefresh.lvtd.dev",
    )
    seen = []

    def endpoint(request):
        seen.append(request.body)
        return HttpResponse("ok")

    response = CanonicalHostMiddleware(endpoint)(request)
    assert response.status_code == 200
    assert seen == [b'{"type":"test"}']
