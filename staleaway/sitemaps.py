from datetime import date

from django.contrib import sitemaps
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse

from core.choices import BlogPostStatus
from core.models import BlogPost


class StaticViewSitemap(sitemaps.Sitemap):
    """Generate Sitemap for the site"""

    priority = 0.9
    protocol = "https"

    def items(self):
        """Identify items that will be in the Sitemap

        Returns:
            List: urlNames that will be in the Sitemap
        """
        return [
            "landing_page",
            "uses",
            "blog_posts",
            "tools",
            "content_review_planner",
            "for_nonprofits",
        ]

    def lastmod(self, item):
        if item == "tools":
            return date(2026, 10, 28)
        if item in {"landing_page", "for_nonprofits"}:
            return date(2026, 10, 23)
        if item == "content_review_planner":
            return date(2026, 10, 30)
        return None

    def location(self, item):
        """Get location for each item in the Sitemap

        Args:
            item (str): Item from the items function

        Returns:
            str: Url for the sitemap item
        """
        return reverse(item)


sitemaps = {
    "static": StaticViewSitemap,
    "blog": GenericSitemap(
        {
            "queryset": BlogPost.objects.filter(status=BlogPostStatus.PUBLISHED).order_by("pk"),
            "date_field": "updated_at",
        },
        priority=0.85,
        protocol="https",
    ),
}
