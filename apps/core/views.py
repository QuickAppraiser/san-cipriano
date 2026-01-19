"""
Core views - Homepage and main pages
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from apps.visitors.models import VisitorInquiry, VisitorCounter


class HomeView(TemplateView):
    """
    Homepage view with hero, welcome message, and main CTA.
    """

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get visitor counter
        counter = VisitorCounter.get_counter()
        context["visitor_count"] = counter.total_count

        return context


class ProtectionView(TemplateView):
    """
    Reserve protection rules and guidelines.
    """

    template_name = "core/protection.html"


class SafetyView(TemplateView):
    """
    Safety rules and important warnings.
    """

    template_name = "core/safety.html"


class RobotsTxtView(View):
    """
    robots.txt for SEO - tells search engines what to crawl.
    """

    def get(self, request):
        lines = [
            "User-agent: *",
            "Allow: /",
            "",
            "# Disallow admin and API",
            "Disallow: /admin/",
            "Disallow: /api/",
            "",
            "# Sitemap",
            f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")


class GoogleVerificationView(View):
    """
    Google Search Console verification file.
    Replace GOOGLE_VERIFICATION_CODE with your actual code from Google Search Console.
    """

    def get(self, request, verification_code):
        # Google expects the file to contain: google-site-verification: googleXXXXXXXXXXXX.html
        content = f"google-site-verification: {verification_code}.html"
        return HttpResponse(content, content_type="text/html")
