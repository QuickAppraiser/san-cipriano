"""
Context processors for global template variables.
"""

from django.conf import settings

from .models import SiteConfiguration


def site_settings(request):
    """
    Add site configuration to all templates.
    """
    try:
        config = SiteConfiguration.get_config()
    except Exception:
        config = None

    return {
        "site_config": config,
        "site_name": getattr(config, "site_name", settings.SITE_NAME),
        "site_tagline": getattr(config, "tagline", settings.SITE_TAGLINE),
        "community_whatsapp": getattr(config, "community_whatsapp", settings.COMMUNITY_WHATSAPP),
        "community_email": getattr(config, "community_email", settings.COMMUNITY_EMAIL),
        "available_languages": settings.LANGUAGES,
    }
