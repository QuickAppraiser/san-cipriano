"""
Content API URL configuration
"""

from django.urls import path

from . import api_views

app_name = "content_api"

urlpatterns = [
    path("biodiversity/", api_views.BiodiversityListAPIView.as_view(), name="biodiversity_list"),
    path("experiences/", api_views.ExperienceListAPIView.as_view(), name="experience_list"),
    path("faq/", api_views.FAQListAPIView.as_view(), name="faq_list"),
]
