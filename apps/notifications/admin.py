from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        "notification_type",
        "recipient",
        "subject",
        "status_badge",
        "created_at",
        "sent_at",
    )
    list_filter = ("notification_type", "status", "created_at")
    search_fields = ("recipient", "subject", "message")
    readonly_fields = (
        "notification_type",
        "recipient",
        "subject",
        "message",
        "status",
        "error_message",
        "inquiry",
        "sent_at",
        "created_at",
    )
    date_hierarchy = "created_at"

    @admin.display(description=_("Estado"))
    def status_badge(self, obj):
        colors = {
            "pendiente": "#ffc107",
            "enviado": "#28a745",
            "fallido": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
