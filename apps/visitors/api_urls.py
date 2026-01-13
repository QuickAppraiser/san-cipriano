"""
Visitors API URL configuration
"""

from django.urls import path

from . import api_views

app_name = "visitors_api"

urlpatterns = [
    path("inquiry/", api_views.InquiryCreateAPIView.as_view(), name="inquiry_create"),
    path("counter/", api_views.VisitorCounterAPIView.as_view(), name="counter"),
]
