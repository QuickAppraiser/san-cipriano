"""
Visitors URL configuration
"""

from django.urls import path

from . import views

app_name = "visitors"

urlpatterns = [
    path("planifica/", views.InquiryFormView.as_view(), name="inquiry_form"),
    path("gracias/", views.ThankYouView.as_view(), name="thank_you"),
    path("servicios/", views.ServicesView.as_view(), name="services"),
]
