"""
Visitors API views
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.utils import get_client_ip
from .models import VisitorInquiry, VisitorCounter
from .serializers import VisitorInquirySerializer, VisitorCounterSerializer


class InquiryCreateAPIView(generics.CreateAPIView):
    """
    API endpoint to create visitor inquiries.
    """

    queryset = VisitorInquiry.objects.all()
    serializer_class = VisitorInquirySerializer

    def perform_create(self, serializer):
        # Save visitor metadata
        serializer.save(
            source_language=self.request.LANGUAGE_CODE or "es",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

        # Increment visitor counter
        counter = VisitorCounter.get_counter()
        counter.increment()


class VisitorCounterAPIView(APIView):
    """
    API endpoint to get current visitor counter.
    """

    def get(self, request):
        counter = VisitorCounter.get_counter()
        serializer = VisitorCounterSerializer(counter)
        return Response(serializer.data)
