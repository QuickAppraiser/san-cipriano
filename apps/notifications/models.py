"""
Notifications models - Log of sent notifications
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class NotificationType(models.TextChoices):
    """Types of notifications."""
    EMAIL = "email", _("Correo Electrónico")
    WHATSAPP = "whatsapp", _("WhatsApp")


class NotificationStatus(models.TextChoices):
    """Status of notifications."""
    PENDING = "pendiente", _("Pendiente")
    SENT = "enviado", _("Enviado")
    FAILED = "fallido", _("Fallido")


class NotificationLog(TimeStampedModel):
    """
    Log of all sent notifications for auditing.
    """

    notification_type = models.CharField(
        _("tipo"),
        max_length=20,
        choices=NotificationType.choices
    )
    recipient = models.CharField(
        _("destinatario"),
        max_length=200,
        help_text=_("Email o número de teléfono")
    )
    subject = models.CharField(
        _("asunto"),
        max_length=200,
        blank=True
    )
    message = models.TextField(_("mensaje"))
    status = models.CharField(
        _("estado"),
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING
    )
    error_message = models.TextField(
        _("mensaje de error"),
        blank=True
    )
    inquiry = models.ForeignKey(
        "visitors.VisitorInquiry",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("consulta"),
        null=True,
        blank=True
    )
    sent_at = models.DateTimeField(_("enviado en"), null=True, blank=True)

    class Meta:
        verbose_name = _("Log de Notificación")
        verbose_name_plural = _("Logs de Notificaciones")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_notification_type_display()} a {self.recipient}"
