"""
Visitors views - Form handling and counter
"""

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView

from apps.core.utils import get_client_ip
from .forms import VisitorInquiryForm
from .models import VisitorInquiry, VisitorCounter


class InquiryFormView(CreateView):
    """
    Main inquiry form view.
    This is the central form that visitors must complete to receive detailed information.
    """

    model = VisitorInquiry
    form_class = VisitorInquiryForm
    template_name = "visitors/inquiry_form.html"
    success_url = reverse_lazy("visitors:thank_you")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Planifica tu Visita")
        context["page_description"] = _(
            "Completa el formulario y recibirás información personalizada "
            "sobre tu visita a San Cipriano."
        )
        return context

    def form_valid(self, form):
        # Save visitor metadata
        form.instance.source_language = self.request.LANGUAGE_CODE
        form.instance.ip_address = get_client_ip(self.request)
        form.instance.user_agent = self.request.META.get("HTTP_USER_AGENT", "")

        response = super().form_valid(form)

        # Increment visitor counter
        counter = VisitorCounter.get_counter()
        counter.increment()

        # Trigger notifications (handled by signals)
        messages.success(
            self.request,
            _("¡Gracias! Hemos recibido tu solicitud. La comunidad te contactará pronto.")
        )

        return response


class ThankYouView(TemplateView):
    """
    Thank you page shown after form submission.
    """

    template_name = "visitors/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("¡Gracias por tu interés!")
        return context


class ServicesView(TemplateView):
    """
    Services overview page (without prices).
    Shows available services with descriptions but no pricing.
    """

    template_name = "visitors/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Servicios")
        context["services"] = [
            {
                "icon": "🏠",
                "name": _("Hospedaje"),
                "description": _("Hoteles y alojamientos comunitarios en armonía con la naturaleza."),
            },
            {
                "icon": "🍽️",
                "name": _("Alimentación"),
                "description": _("Gastronomía local preparada por la comunidad con productos frescos."),
            },
            {
                "icon": "🚃",
                "name": _("Transporte en Brujitas"),
                "description": _("La experiencia única de viajar en los famosos carros sobre rieles."),
            },
            {
                "icon": "🅿️",
                "name": _("Parqueadero"),
                "description": _("Estacionamiento seguro y vigilado para tu vehículo."),
            },
            {
                "icon": "🎫",
                "name": _("Entrada a la Reserva"),
                "description": _("Acceso a los senderos, ríos y espacios naturales de la reserva."),
            },
            {
                "icon": "🧭",
                "name": _("Tours Guiados"),
                "description": _("Recorridos con guías locales que conocen cada rincón de la reserva."),
            },
            {
                "icon": "🌿",
                "name": _("Experiencias Naturales"),
                "description": _("Avistamiento de aves, senderismo, y contacto directo con la biodiversidad."),
            },
        ]
        return context
