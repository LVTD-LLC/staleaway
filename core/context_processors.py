from allauth.socialaccount.models import SocialApp
from django.conf import settings

from core.choices import ProfileStates
from staleaway.utils import get_staleaway_logger

logger = get_staleaway_logger(__name__)


def current_state(request):
    if request.user.is_authenticated:
        return {"current_state": request.user.profile.current_state}
    return {"current_state": ProfileStates.STRANGER}


def posthog_api_key(request):
    """Opt public, anonymous HTML into bounded acquisition measurement only.

    Account/review URLs and authenticated pages can contain private identifiers.
    A template choice alone is not a sufficient boundary: accounts share the
    landing layout, and a nonexistent blog slug must not become an event URL.
    """
    from django.urls import reverse

    from core.choices import BlogPostStatus
    from core.models import BlogPost

    config = None
    match = request.resolver_match
    if settings.POSTHOG_API_KEY and not request.user.is_authenticated and match:
        name = match.url_name
        if name in {"landing_page", "blog_posts", "uses"}:
            path = reverse(name)
        elif name == "blog_post" and BlogPost.objects.filter(
            slug=match.kwargs.get("slug"), status=BlogPostStatus.PUBLISHED
        ).exists():
            path = reverse(name, kwargs={"slug": match.kwargs["slug"]})
        else:
            path = None
        if path:
            config = {
                "api_key": settings.POSTHOG_API_KEY,
                "url": settings.SITE_URL.rstrip("/") + path,
            }
    return {"public_analytics": config}


def available_social_providers(request):
    """
    Checks which social authentication providers are available.
    Returns a list of provider names from either SOCIALACCOUNT_PROVIDERS settings
    or SocialApp database entries, as django-allauth supports both configuration methods.
    """
    available_providers = set()

    configured_providers = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})

    available_providers.update(configured_providers.keys())

    try:
        social_apps = SocialApp.objects.all()
        for social_app in social_apps:
            available_providers.add(social_app.provider)
    except Exception as e:
        logger.warning("Error retrieving SocialApp entries", error=str(e))

    available_providers_list = sorted(list(available_providers))

    return {
        "available_social_providers": available_providers_list,
        "has_social_providers": len(available_providers_list) > 0,
    }


def seo_site(request):
    """Use the configured origin for public canonical and crawler URLs."""
    return {"site_url": settings.SITE_URL.rstrip("/")}
