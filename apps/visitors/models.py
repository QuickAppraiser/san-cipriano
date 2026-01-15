"""
Visitors models - Inquiry form and visitor counter
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class ServiceChoice(models.TextChoices):
    """Available services for visitors."""
    FOOD = "alimentacion", _("Alimentación")
    TRANSPORT = "transporte", _("Transporte en brujitas")
    FOOD_TRANSPORT = "alimentacion_transporte", _("Alimentación + Transporte")
    LODGING = "hospedaje", _("Hospedaje")
    GUIDE = "guia", _("Guía turístico")
    PARKING = "parqueadero", _("Parqueadero")
    ENTRY = "entrada", _("Entrada a la reserva")
    TOURS = "tours", _("Tours guiados")
    EXPERIENCES = "experiencias", _("Experiencias naturales")
    OTHER = "otro", _("Otros")


class InquiryStatus(models.TextChoices):
    """Status of visitor inquiry."""
    PENDING = "pendiente", _("Pendiente")
    CONTACTED = "contactado", _("Contactado")
    CONFIRMED = "confirmado", _("Confirmado")
    COMPLETED = "completado", _("Completado")
    CANCELLED = "cancelado", _("Cancelado")


class VisitorInquiry(TimeStampedModel):
    """
    Visitor inquiry form submission.
    Stores contact information and service interests.
    """

    # Personal Information
    full_name = models.CharField(
        _("nombre completo"),
        max_length=200
    )
    phone = models.CharField(
        _("teléfono / WhatsApp"),
        max_length=20
    )
    email = models.EmailField(_("correo electrónico"))
    city = models.CharField(
        _("ciudad"),
        max_length=100
    )
    country = models.CharField(
        _("país"),
        max_length=100,
        default="Colombia"
    )

    # Visit Details
    estimated_arrival = models.DateField(
        _("fecha estimada de llegada"),
        null=True,
        blank=True
    )
    estimated_departure = models.DateField(
        _("fecha estimada de salida"),
        null=True,
        blank=True
    )
    number_of_people = models.PositiveIntegerField(
        _("número de personas"),
        default=1
    )
    number_of_children = models.PositiveIntegerField(
        _("número de menores"),
        default=0,
        help_text=_("Menores de 18 años")
    )

    # Services (stored as JSON array)
    services = models.JSONField(
        _("servicios seleccionados"),
        default=list,
        help_text=_("Lista de servicios de interés")
    )

    # Additional Information
    special_requests = models.TextField(
        _("solicitudes especiales"),
        blank=True,
        help_text=_("Alergias, necesidades especiales, preguntas, etc.")
    )

    # Status Tracking
    status = models.CharField(
        _("estado"),
        max_length=20,
        choices=InquiryStatus.choices,
        default=InquiryStatus.PENDING
    )
    notes = models.TextField(
        _("notas internas"),
        blank=True,
        help_text=_("Notas del equipo de la comunidad")
    )

    # Notifications
    whatsapp_notified = models.BooleanField(
        _("notificado por WhatsApp"),
        default=False
    )
    email_notified = models.BooleanField(
        _("notificado por email"),
        default=False
    )

    # Source tracking
    source_language = models.CharField(
        _("idioma de origen"),
        max_length=5,
        default="es"
    )
    ip_address = models.GenericIPAddressField(
        _("dirección IP"),
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        _("user agent"),
        blank=True
    )

    class Meta:
        verbose_name = _("Consulta de Visitante")
        verbose_name_plural = _("Consultas de Visitantes")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def services_display(self):
        """Return human-readable service names."""
        service_dict = dict(ServiceChoice.choices)
        return [service_dict.get(s, s) for s in self.services]

    @property
    def total_people(self):
        """Total number of people including children."""
        return self.number_of_people


class VisitorCounter(models.Model):
    """
    Singleton model for tracking visitor interest count.
    Displays: "Personas interesadas en conocer San Cipriano"
    """

    base_count = models.PositiveIntegerField(
        _("contador base"),
        default=45,
        help_text=_("Número inicial del contador")
    )
    inquiry_count = models.PositiveIntegerField(
        _("consultas recibidas"),
        default=0,
        help_text=_("Número de formularios enviados")
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contador de Visitantes")
        verbose_name_plural = _("Contador de Visitantes")

    def __str__(self):
        return f"Contador: {self.total_count}"

    @property
    def total_count(self):
        """Total count displayed to visitors."""
        return self.base_count + self.inquiry_count

    def increment(self):
        """Increment the inquiry count."""
        self.inquiry_count += 1
        self.save(update_fields=["inquiry_count", "last_updated"])

    @classmethod
    def get_counter(cls):
        """Get or create the visitor counter."""
        counter, created = cls.objects.get_or_create(pk=1)
        if created:
            counter.base_count = getattr(
                settings, "VISITOR_COUNTER_INITIAL", 45
            )
            counter.save()
        return counter
