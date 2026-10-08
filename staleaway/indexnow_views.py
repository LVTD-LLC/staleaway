"""Public IndexNow ownership proof and deployment marker (not credentials)."""

from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe

KEY = "ec359f3562d64321a0739047520bed5294d5f3cffff7a3a70b41f2cf76e630b1"


@never_cache
@require_safe
def ownership_key(request):
    return HttpResponse(KEY + "\n", content_type="text/plain; charset=utf-8")


@never_cache
@require_safe
def deployment_revision(request):
    marker = Path(settings.BASE_DIR) / "deployment-revision.txt"
    revision = marker.read_text().strip() if marker.exists() else "development"
    return HttpResponse(revision + "\n", content_type="text/plain; charset=utf-8")
