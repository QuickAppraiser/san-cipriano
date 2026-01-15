"""
Core URL configuration
"""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("proteccion/", views.ProtectionView.as_view(), name="protection"),
    path("seguridad/", views.SafetyView.as_view(), name="safety"),
    path("terminos/", views.TermsView.as_view(), name="terms"),
]
