from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from allauth.account.views import SignupView
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django_q.tasks import async_task

from staleaway.utils import get_staleaway_logger
from core.forms import ProfileUpdateForm, SitemapForm, SitemapSettingsForm
from core.models import BlogPost, Feedback, Page, Profile, Sitemap


logger = get_staleaway_logger(__name__)


class LandingPageView(TemplateView):
    template_name = "pages/landing-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and settings.POSTHOG_API_KEY:
            user = self.request.user
            profile = user.profile

            async_task(
                "core.tasks.try_create_posthog_alias",
                profile_id=profile.id,
                cookies=self.request.COOKIES,
                source_function="LandingPageView - get_context_data",
                group="Create Posthog Alias",
            )

        return context


class HomeView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    login_url = "account_login"
    template_name = "pages/home.html"
    success_message = "Sitemap URL added successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SitemapForm()
        context["sitemaps"] = Sitemap.objects.filter(profile=self.request.user.profile).order_by(
            "-created_at"
        )
        return context

    def post(self, request, *args, **kwargs):
        form = SitemapForm(request.POST)
        if form.is_valid():
            sitemap = form.save(commit=False)
            sitemap.profile = request.user.profile
            sitemap.save()

            logger.info(
                "Sitemap URL added",
                profile_id=request.user.profile.id,
                email=request.user.email,
                sitemap_url=sitemap.sitemap_url,
            )

            messages.success(request, self.success_message)
            return redirect("home")
        else:
            context = self.get_context_data(**kwargs)
            context["form"] = form
            return self.render_to_response(context)


class SitemapDetailView(LoginRequiredMixin, DetailView):
    login_url = "account_login"
    model = Sitemap
    template_name = "pages/sitemap_detail.html"
    context_object_name = "sitemap"

    def get_queryset(self):
        return Sitemap.objects.filter(profile=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pages"] = Page.objects.filter(sitemap=self.object).order_by("-needs_review", "url")
        return context


class AccountSignupView(SignupView):
    template_name = "account/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.user
        profile = user.profile

        async_task(
            "core.tasks.try_create_posthog_alias",
            profile_id=profile.id,
            cookies=self.request.COOKIES,
            source_function="AccountSignupView - form_valid",
            group="Create Posthog Alias",
        )

        async_task(
            "core.tasks.track_event",
            profile_id=profile.id,
            event_name="user_signed_up",
            properties={
                "$set": {
                    "email": profile.user.email,
                    "username": profile.user.username,
                },
            },
            source_function="AccountSignupView - form_valid",
            group="Track Event",
        )

        return response


class UserSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "account_login"
    model = Profile
    form_class = ProfileUpdateForm
    success_message = "User Profile Updated"
    success_url = reverse_lazy("settings")
    template_name = "pages/user-settings.html"

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        from core.forms import get_timezone_list
        from core.models import EmailPreference

        context = super().get_context_data(**kwargs)
        user = self.request.user

        primary_email = EmailAddress.objects.get_for_user(user, user.email)
        context["email_verified"] = primary_email.verified
        context["resend_confirmation_url"] = reverse("resend_confirmation")

        sitemaps = Sitemap.objects.filter(profile=user.profile).order_by("-created_at")
        sitemap_forms = {}
        for sitemap in sitemaps:
            sitemap_forms[sitemap.id] = SitemapSettingsForm(
                instance=sitemap, prefix=f"sitemap_{sitemap.id}"
            )

        context["sitemaps"] = sitemaps
        context["sitemap_forms"] = sitemap_forms
        context["timezones"] = get_timezone_list()
        context["email_preferences"] = EmailPreference.objects.filter(
            profile=user.profile
        ).order_by("-created_at")

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile_form = self.get_form()

        sitemaps = Sitemap.objects.filter(profile=request.user.profile)
        sitemap_forms = []
        for sitemap in sitemaps:
            sitemap_forms.append(
                (
                    sitemap,
                    SitemapSettingsForm(
                        request.POST, instance=sitemap, prefix=f"sitemap_{sitemap.id}"
                    ),
                )
            )

        profile_valid = profile_form.is_valid()
        sitemap_forms_valid = all(form.is_valid() for _, form in sitemap_forms)

        if profile_valid and sitemap_forms_valid:
            profile_form.save()

            logger.info(
                "User profile updated", profile_id=request.user.profile.id, email=request.user.email
            )

            updated_count = 0
            for sitemap, form in sitemap_forms:
                form.save()
                updated_count += 1

                logger.info(
                    "Sitemap settings updated",
                    profile_id=request.user.profile.id,
                    email=request.user.email,
                    sitemap_id=sitemap.id,
                    pages_per_review=sitemap.pages_per_review,
                    review_cadence=sitemap.review_cadence,
                )

            messages.success(request, "Settings updated successfully")
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(profile_form)


@login_required
def resend_confirmation_email(request):
    user = request.user
    send_email_confirmation(request, user, EmailAddress.objects.get_for_user(user, user.email))

    return redirect("settings")


class BlogView(ListView):
    model = BlogPost
    template_name = "blog/blog_posts.html"
    context_object_name = "blog_posts"


class BlogPostView(DetailView):
    model = BlogPost
    template_name = "blog/blog_post.html"
    context_object_name = "blog_post"


@login_required
def review_page_redirect(request, page_id):
    from django.utils import timezone

    try:
        page = Page.objects.get(id=page_id, profile=request.user.profile)

        page.reviewed = True
        page.reviewed_at = timezone.now()
        page.save(update_fields=["reviewed", "reviewed_at"])

        return redirect(page.url)
    except Page.DoesNotExist:
        messages.error(request, "Page not found or you don't have permission to access it.")
        return redirect("home")


class AdminPanelView(UserPassesTestMixin, TemplateView):
    template_name = "pages/admin-panel.html"
    login_url = "account_login"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect("home")

    def get_context_data(self, **kwargs):
        from datetime import timedelta

        from django.contrib.auth.models import User
        from django.db.models import Count
        from django.utils import timezone

        context = super().get_context_data(**kwargs)

        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        total_users = User.objects.count()
        total_profiles = Profile.objects.count()
        total_sitemaps = Sitemap.objects.count()
        total_pages = Page.objects.count()
        total_feedback = Feedback.objects.count()

        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        new_users_month = User.objects.filter(date_joined__gte=month_ago).count()

        users_with_sitemaps = Profile.objects.filter(sitemap__isnull=False).distinct().count()

        pages_reviewed = Page.objects.filter(reviewed=True).count()
        pages_unreviewed = Page.objects.filter(reviewed=False).count()

        recent_users = User.objects.select_related("profile").order_by("-date_joined")[:10]
        recent_feedback = Feedback.objects.select_related("profile__user").order_by("-created_at")[
            :10
        ]
        recent_sitemaps = Sitemap.objects.select_related("profile__user").order_by("-created_at")[
            :10
        ]

        top_users_by_pages = (
            Profile.objects.annotate(page_count=Count("pages"))
            .filter(page_count__gt=0)
            .order_by("-page_count")[:10]
        )

        context.update(
            {
                "total_users": total_users,
                "total_profiles": total_profiles,
                "total_sitemaps": total_sitemaps,
                "total_pages": total_pages,
                "total_feedback": total_feedback,
                "new_users_week": new_users_week,
                "new_users_month": new_users_month,
                "users_with_sitemaps": users_with_sitemaps,
                "pages_reviewed": pages_reviewed,
                "pages_unreviewed": pages_unreviewed,
                "recent_users": recent_users,
                "recent_feedback": recent_feedback,
                "recent_sitemaps": recent_sitemaps,
                "top_users_by_pages": top_users_by_pages,
            }
        )

        logger.info(
            "Admin panel accessed",
            email=self.request.user.email,
            profile_id=self.request.user.profile.id,
        )

        return context


@staff_member_required
def send_test_email(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect("home")

    if request.method == "POST":
        profile_id = request.user.profile.id

        async_task(
            "core.tasks.send_page_email_to_profile",
            profile_id=profile_id,
            group="Send Test Email",
        )

        logger.info(
            "Test email queued",
            email=request.user.email,
            profile_id=profile_id,
        )

        messages.success(request, f"Test email queued and will be sent to {request.user.email}!")

    return redirect("admin_panel")


@staff_member_required
def trigger_schedule_review_emails(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect("home")

    if request.method == "POST":
        async_task(
            "core.tasks.schedule_review_emails",
            group="Schedule Review Emails",
        )

        logger.info(
            "Schedule review emails task triggered",
            email=request.user.email,
            profile_id=request.user.profile.id,
        )

        messages.success(request, "Review email scheduling task has been queued!")

    return redirect("admin_panel")


@staff_member_required
def trigger_schedule_sitemap_reparse(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect("home")

    if request.method == "POST":
        async_task(
            "core.tasks.schedule_sitemap_reparse",
            group="Schedule Sitemap Reparse",
        )

        logger.info(
            "Schedule sitemap reparse task triggered",
            email=request.user.email,
            profile_id=request.user.profile.id,
        )

        messages.success(request, "Sitemap reparse scheduling task has been queued!")

    return redirect("admin_panel")
