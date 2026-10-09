"""staleaway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from staleaway.indexnow_views import deployment_revision, ownership_key
from staleaway.sitemaps import sitemaps

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("indexnow-key.txt", ownership_key, name="indexnow_key"),
    path("deployment.txt", deployment_revision, name="deployment_revision"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("anymail/", include("anymail.urls")),
    path("uses", TemplateView.as_view(template_name="pages/uses.html"), name="uses"),
    path("", include("core.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps, "template_name": "sitemap.xml"},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
