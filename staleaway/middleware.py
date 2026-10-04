from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    """Move browser links without redirecting signed webhook/API POST bodies."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in {"GET", "HEAD"} and request.get_host() in settings.LEGACY_HOSTS:
            return HttpResponsePermanentRedirect(
                settings.SITE_URL.rstrip("/") + request.get_full_path()
            )
        return self.get_response(request)
