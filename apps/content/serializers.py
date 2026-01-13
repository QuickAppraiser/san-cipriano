"""
Content serializers for API
"""

from rest_framework import serializers

from .models import BiodiversityEntry, Experience, FAQ


class BiodiversityEntrySerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = BiodiversityEntry
        fields = [
            "id",
            "name",
            "scientific_name",
            "category",
            "category_display",
            "description",
            "conservation_status",
            "image",
            "is_featured",
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "name",
            "description",
            "duration_info",
            "difficulty",
            "icon",
            "image",
            "is_featured",
        ]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer"]
