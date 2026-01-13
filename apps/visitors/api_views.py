"""
Visitors API views
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

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
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

        # Increment visitor counter
        counter = VisitorCounter.get_counter()
        counter.increment()

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return self.request.META.get("REMOTE_ADDR")


class VisitorCounterAPIView(APIView):
    """
    API endpoint to get current visitor counter.
    """

    def get(self, request):
        counter = VisitorCounter.get_counter()
        serializer = VisitorCounterSerializer(counter)
        return Response(serializer.data)
