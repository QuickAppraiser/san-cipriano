"""
Core models - Base models and site configuration
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Abstract base model with created and updated timestamps.
    """

    created_at = models.DateTimeField(_("creado"), auto_now_add=True)
    updated_at = models.DateTimeField(_("actualizado"), auto_now=True)

    class Meta:
        abstract = True


class SiteConfiguration(models.Model):
    """
    Singleton model for site-wide configuration.
    """

    site_name = models.CharField(
        _("nombre del sitio"),
        max_length=100,
        default="San Cipriano"
    )
    tagline = models.CharField(
        _("eslogan"),
        max_length=200,
        default="Reserva Natural Comunitaria"
    )
    welcome_message = models.TextField(
        _("mensaje de bienvenida"),
        default="Bienvenidos a San Cipriano, una reserva natural cuidada por su comunidad."
    )
    community_whatsapp = models.CharField(
        _("WhatsApp de la comunidad"),
        max_length=20,
        default="+573113111669"
    )
    community_email = models.EmailField(
        _("correo de la comunidad"),
        default="lordmauricio22@gmail.com"
    )
    visitor_counter_base = models.PositiveIntegerField(
        _("contador base de visitantes"),
        default=180,
        help_text=_("Número base para el contador de visitantes interesados")
    )
    is_active = models.BooleanField(_("activo"), default=True)

    class Meta:
        verbose_name = _("Configuración del Sitio")
        verbose_name_plural = _("Configuración del Sitio")

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one configuration exists
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValueError(_("Solo puede existir una configuración del sitio"))
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        """Get or create the site configuration."""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
