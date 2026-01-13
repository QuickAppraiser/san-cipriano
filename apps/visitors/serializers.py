"""
Visitors serializers for API
"""

from rest_framework import serializers

from .models import VisitorInquiry, VisitorCounter, ServiceChoice


class VisitorInquirySerializer(serializers.ModelSerializer):
    """
    Serializer for visitor inquiry form submissions.
    """

    services = serializers.MultipleChoiceField(
        choices=ServiceChoice.choices,
        required=True
    )

    class Meta:
        model = VisitorInquiry
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "city",
            "country",
            "estimated_arrival",
            "estimated_departure",
            "number_of_people",
            "number_of_children",
            "services",
            "special_requests",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_services(self, value):
        """Convert to list for JSON storage."""
        return list(value)


class VisitorCounterSerializer(serializers.ModelSerializer):
    """
    Serializer for visitor counter.
    """

    total_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VisitorCounter
        fields = ["total_count", "last_updated"]
