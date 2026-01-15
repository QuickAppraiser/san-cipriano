"""
Simple URL configuration for San Cipriano project.
No database, no admin, no registration - just static pages.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView


# Simple template views - no database needed
class HomeView(TemplateView):
    template_name = "core/home_simple.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Inicio"
        # Static experiences for homepage
        context["experiences"] = [
            {"icon": "🐦", "name": "Avistamiento de Aves", "description": "Más de 200 especies de aves en su hábitat natural."},
            {"icon": "🚶", "name": "Senderismo", "description": "Recorre senderos en medio de la selva tropical."},
            {"icon": "🏊", "name": "Baño en Río", "description": "Aguas cristalinas del río San Cipriano."},
            {"icon": "🚃", "name": "Paseo en Brujita", "description": "La experiencia única de viajar en los famosos carros sobre rieles."},
        ]
        context["gallery_images"] = []  # Will use media folder images
        return context


class AboutView(TemplateView):
    template_name = "content/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Sobre Nosotros"
        return context


class ProtectionView(TemplateView):
    template_name = "core/protection.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Protección de la Reserva"
        return context


class SafetyView(TemplateView):
    template_name = "core/safety.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Seguridad y Normas"
        return context


class BiodiversityView(TemplateView):
    template_name = "content/biodiversity_simple.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Biodiversidad"
        # Static biodiversity data
        context["biodiversity_by_category"] = {
            "Aves": [
                {"name": "Tucán", "scientific_name": "Ramphastos", "description": "Ave colorida con pico grande característico."},
                {"name": "Colibrí", "scientific_name": "Trochilidae", "description": "Pequeña ave que puede volar en todas direcciones."},
                {"name": "Guacamaya", "scientific_name": "Ara", "description": "Ave de colores brillantes de la familia de los loros."},
            ],
            "Mamíferos": [
                {"name": "Mono Aullador", "scientific_name": "Alouatta", "description": "Primate conocido por su potente vocalización."},
                {"name": "Perezoso", "scientific_name": "Bradypus", "description": "Mamífero arbóreo de movimientos lentos."},
            ],
            "Anfibios": [
                {"name": "Rana Venenosa", "scientific_name": "Dendrobatidae", "description": "Pequeña rana de colores brillantes."},
            ],
            "Flora": [
                {"name": "Orquídea", "scientific_name": "Orchidaceae", "description": "Flor exótica de gran belleza."},
                {"name": "Heliconia", "scientific_name": "Heliconia", "description": "Planta tropical con flores coloridas."},
            ],
        }
        return context


class ServicesView(TemplateView):
    template_name = "visitors/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Servicios"
        context["services"] = [
            {"icon": "🏠", "name": "Hospedaje", "description": "Hoteles y alojamientos comunitarios en armonía con la naturaleza."},
            {"icon": "🍽️", "name": "Alimentación", "description": "Gastronomía local preparada por la comunidad con productos frescos."},
            {"icon": "🚃", "name": "Transporte en Brujitas", "description": "La experiencia única de viajar en los famosos carros sobre rieles."},
            {"icon": "🅿️", "name": "Parqueadero", "description": "Estacionamiento seguro y vigilado para tu vehículo."},
            {"icon": "🎫", "name": "Entrada a la Reserva", "description": "Acceso a los senderos, ríos y espacios naturales de la reserva."},
            {"icon": "🧭", "name": "Tours Guiados", "description": "Recorridos con guías locales que conocen cada rincón de la reserva."},
            {"icon": "🌿", "name": "Experiencias Naturales", "description": "Avistamiento de aves, senderismo, y contacto directo con la biodiversidad."},
        ]
        return context


class ContactView(TemplateView):
    template_name = "content/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contacto"
        return context


class FAQView(TemplateView):
    template_name = "content/faq_simple.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Preguntas Frecuentes"
        context["faqs"] = [
            {"question": "¿Cómo llego a San Cipriano?", "answer": "Desde Cali, toma la vía al mar hasta Córdoba. Allí tomas una 'brujita' (carro sobre rieles) que te lleva directamente a San Cipriano en aproximadamente 30 minutos."},
            {"question": "¿Qué debo llevar?", "answer": "Ropa cómoda de colores claros, manga larga para protección contra insectos, traje de baño, gorra o sombrero (NO protector solar ni repelente químico - contaminan el río), careta de snorkel, zapatos para agua, y una bolsa para tu basura."},
            {"question": "¿Es seguro visitar San Cipriano?", "answer": "Sí, San Cipriano es un destino seguro. La comunidad local cuida de los visitantes y hay guías disponibles para acompañarte."},
            {"question": "¿Cuál es la mejor época para visitar?", "answer": "Puedes visitar todo el año. La temporada seca (diciembre-marzo y julio-agosto) es ideal, pero la temporada de lluvias también tiene su encanto."},
            {"question": "¿Hay señal de celular?", "answer": "La señal es limitada. Algunas áreas tienen cobertura de Claro y Movistar, pero recomendamos desconectarse y disfrutar de la naturaleza."},
            {"question": "¿Puedo llevar mascotas?", "answer": "No se recomienda llevar mascotas para proteger la fauna local y garantizar tu comodidad durante los recorridos."},
        ]
        return context


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("nosotros/", AboutView.as_view(), name="about"),
    path("proteccion/", ProtectionView.as_view(), name="protection"),
    path("seguridad/", SafetyView.as_view(), name="safety"),
    path("biodiversidad/", BiodiversityView.as_view(), name="biodiversity"),
    path("servicios/", ServicesView.as_view(), name="services"),
    path("contacto/", ContactView.as_view(), name="contact"),
    path("faq/", FAQView.as_view(), name="faq"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
