"""
Content API views
"""

from rest_framework import generics

from .models import BiodiversityEntry, Experience, FAQ
from .serializers import BiodiversityEntrySerializer, ExperienceSerializer, FAQSerializer


class BiodiversityListAPIView(generics.ListAPIView):
    """
    API endpoint for biodiversity entries.
    """

    queryset = BiodiversityEntry.objects.filter(is_active=True)
    serializer_class = BiodiversityEntrySerializer


class ExperienceListAPIView(generics.ListAPIView):
    """
    API endpoint for experiences.
    """

    queryset = Experience.objects.filter(is_active=True)
    serializer_class = ExperienceSerializer


class FAQListAPIView(generics.ListAPIView):
    """
    API endpoint for FAQs.
    """

    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
