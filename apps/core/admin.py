from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("site_name", "community_whatsapp", "community_email", "is_active")
    fieldsets = (
        (_("Identidad"), {
            "fields": ("site_name", "tagline", "welcome_message")
        }),
        (_("Contacto"), {
            "fields": ("community_whatsapp", "community_email")
        }),
        (_("Configuración"), {
            "fields": ("visitor_counter_base", "is_active")
        }),
    )

    def has_add_permission(self, request):
        # Only allow one configuration
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
