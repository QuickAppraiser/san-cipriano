from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import VisitorInquiry, VisitorCounter


@admin.register(VisitorInquiry)
class VisitorInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "email",
        "number_of_people",
        "estimated_arrival",
        "status_badge",
        "created_at",
    )
    list_filter = ("status", "created_at", "country")
    search_fields = ("full_name", "email", "phone", "city")
    readonly_fields = (
        "created_at",
        "updated_at",
        "ip_address",
        "user_agent",
        "source_language",
    )
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = (
        (_("Información Personal"), {
            "fields": ("full_name", "phone", "email", "city", "country")
        }),
        (_("Detalles de Visita"), {
            "fields": (
                "estimated_arrival",
                "estimated_departure",
                "number_of_people",
                "number_of_children",
                "services",
                "special_requests",
            )
        }),
        (_("Estado"), {
            "fields": ("status", "notes", "whatsapp_notified", "email_notified")
        }),
        (_("Metadata"), {
            "fields": ("source_language", "ip_address", "user_agent", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    actions = ["mark_as_contacted", "mark_as_confirmed"]

    @admin.display(description=_("Estado"))
    def status_badge(self, obj):
        colors = {
            "pendiente": "#ffc107",
            "contactado": "#17a2b8",
            "confirmado": "#28a745",
            "completado": "#6c757d",
            "cancelado": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description=_("Marcar como contactado"))
    def mark_as_contacted(self, request, queryset):
        queryset.update(status="contactado")

    @admin.action(description=_("Marcar como confirmado"))
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status="confirmado")


@admin.register(VisitorCounter)
class VisitorCounterAdmin(admin.ModelAdmin):
    list_display = ("total_count", "base_count", "inquiry_count", "last_updated")
    readonly_fields = ("inquiry_count", "last_updated")

    def has_add_permission(self, request):
        return not VisitorCounter.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
