from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import BiodiversityEntry, Experience, GalleryImage, FAQ


@admin.register(BiodiversityEntry)
class BiodiversityEntryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "scientific_name",
        "category",
        "conservation_status",
        "is_featured",
        "is_active",
    )
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("name", "scientific_name", "description")
    list_editable = ("is_featured", "is_active")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "icon_display",
        "name",
        "duration_info",
        "difficulty",
        "is_featured",
        "is_active",
        "order",
    )
    list_filter = ("is_featured", "is_active")
    search_fields = ("name", "description")
    list_editable = ("is_featured", "is_active", "order")
    ordering = ["order"]

    @admin.display(description="")
    def icon_display(self, obj):
        return format_html('<span style="font-size: 24px;">{}</span>', obj.icon)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "is_hero", "is_active", "order", "created_at")
    list_filter = ("is_hero", "is_active")
    list_editable = ("is_hero", "is_active", "order")
    ordering = ["order"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question_short", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("question", "answer")
    list_editable = ("is_active", "order")
    ordering = ["order"]

    @admin.display(description=_("Pregunta"))
    def question_short(self, obj):
        return obj.question[:80] + "..." if len(obj.question) > 80 else obj.question
