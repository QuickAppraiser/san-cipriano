"""
Content URL configuration
"""

from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("sobre/", views.AboutView.as_view(), name="about"),
    path("biodiversidad/", views.BiodiversityView.as_view(), name="biodiversity"),
    path("preguntas/", views.FAQView.as_view(), name="faq"),
    path("contacto/", views.ContactView.as_view(), name="contact"),
]
