"""
Content views - Static pages
"""

from django.views.generic import TemplateView, ListView

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


class BiodiversityView(ListView):
    """
    Biodiversity and experiences page.
    """

    model = BiodiversityEntry
    template_name = "content/biodiversity.html"
    context_object_name = "entries"

    def get_queryset(self):
        return BiodiversityEntry.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Biodiversidad y Experiencias"

        # Group entries by category
        context["categories"] = {}
        for cat_value, cat_label in BiodiversityCategory.choices:
            entries = self.get_queryset().filter(category=cat_value)
            if entries.exists():
                context["categories"][cat_label] = entries

        # Add experiences
        context["experiences"] = Experience.objects.filter(is_active=True)

        return context


class FAQView(ListView):
    """
    Frequently asked questions page.
    """

    model = FAQ
    template_name = "content/faq.html"
    context_object_name = "faqs"

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Preguntas Frecuentes"
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
