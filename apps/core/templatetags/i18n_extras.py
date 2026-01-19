"""
Custom template tags for internationalization.
"""

from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag
def translate_url_tag(url, lang_code):
    """
    Translate a URL to a different language.
    Usage: {% translate_url_tag request.path 'en' %}
    """
    return translate_url(url, lang_code)
