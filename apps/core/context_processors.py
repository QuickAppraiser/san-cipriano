"""
Context processors for global template variables.
"""

import re
from django.conf import settings
from django.utils.translation import get_language


def site_settings(request):
    """
    Add site configuration to all templates.
    Works without database - uses settings directly.
    """
    # Try to load from database if available, otherwise use settings
    config = None
    try:
        from .models import SiteConfiguration
        config = SiteConfiguration.get_config()
    except Exception:
        pass

    # Get dynamic visitor count from database
    visitor_count = getattr(settings, "VISITOR_COUNTER_INITIAL", 180)
    try:
        from apps.visitors.models import VisitorCounter
        counter = VisitorCounter.get_counter()
        visitor_count = counter.total_count
    except Exception:
        pass

    # Build translated URLs for language switcher
    languages_with_urls = []
    current_path = request.path

    # Get all language codes
    all_lang_codes = [code for code, name in getattr(settings, "LANGUAGES", [("es", "Español")])]

    # Strip any existing language prefix from the path
    # This regex matches /xx/ at the start where xx is a valid language code
    lang_prefix_pattern = r'^/(' + '|'.join(all_lang_codes) + ')/'
    base_path = re.sub(lang_prefix_pattern, '/', current_path)

    for lang_code, lang_name in getattr(settings, "LANGUAGES", [("es", "Español")]):
        # Spanish (default) has no prefix, other languages get prefix
        if lang_code == 'es':
            translated_path = base_path
        else:
            translated_path = f'/{lang_code}{base_path}'

        languages_with_urls.append({
            'code': lang_code,
            'name': lang_name,
            'url': translated_path,
        })

    return {
        "site_config": config,
        "site_name": getattr(config, "site_name", None) or getattr(settings, "SITE_NAME", "San Cipriano"),
        "site_tagline": getattr(config, "tagline", None) or getattr(settings, "SITE_TAGLINE", "Reserva Natural Comunitaria"),
        "community_whatsapp": getattr(config, "community_whatsapp", None) or getattr(settings, "COMMUNITY_WHATSAPP", "+573113111669"),
        "community_email": getattr(config, "community_email", None) or getattr(settings, "COMMUNITY_EMAIL", "lordmauricio22@gmail.com"),
        "available_languages": getattr(settings, "LANGUAGES", [("es", "Español")]),
        "languages_with_urls": languages_with_urls,
        "visitor_count": visitor_count,
    }
