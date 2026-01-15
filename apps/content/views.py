"""
Content views - Static pages
"""

from django.views.generic import TemplateView

from .models import BiodiversityEntry, Experience, FAQ, BiodiversityCategory


class AboutView(TemplateView):
    """
    About San Cipriano page.
    History, location, community focus.
    """

    template_name = "content/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Sobre San Cipriano"
        return context


class BiodiversityView(TemplateView):
    """
    Biodiversity and experiences page.
    Uses TemplateView to avoid database dependency.
    """

    template_name = "content/biodiversity.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Biodiversidad y Experiencias"
        context["entries"] = []
        context["categories"] = {}
        context["experiences"] = []

        # Try to load from database, but don't fail if tables don't exist
        try:
            entries = BiodiversityEntry.objects.filter(is_active=True)
            context["entries"] = entries

            # Group entries by category
            for cat_value, cat_label in BiodiversityCategory.choices:
                cat_entries = entries.filter(category=cat_value)
                if cat_entries.exists():
                    context["categories"][cat_label] = cat_entries

            # Add experiences
            context["experiences"] = Experience.objects.filter(is_active=True)
        except Exception:
            # Database tables don't exist yet - template will show static content
            pass

        return context


class FAQView(TemplateView):
    """
    Frequently asked questions page.
    Uses TemplateView to avoid database dependency.
    """

    template_name = "content/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Preguntas Frecuentes"
        context["faqs"] = []

        # Try to load from database, but don't fail if tables don't exist
        try:
            context["faqs"] = FAQ.objects.filter(is_active=True)
        except Exception:
            pass

        return context


class ContactView(TemplateView):
    """
    Contact page with WhatsApp and email info.
    """

    template_name = "content/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contacto"
        return context
