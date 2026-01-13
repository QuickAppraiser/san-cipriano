"""
Core views - Homepage and main pages
"""

from django.shortcuts import render
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
