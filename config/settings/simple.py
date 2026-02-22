"""
Django SIMPLE settings for San Cipriano project.
No database, no admin, no registration - just static pages with templates.
"""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = "simple-dev-key-not-for-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Minimal apps - no database-dependent apps
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

# Minimal middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls_simple"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

# No database needed
DATABASES = {}

# Internationalization
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_L10N = True

LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("it", "Italiano"),
    ("pt", "Português"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Site info (used by context processor)
SITE_NAME = "San Cipriano"
SITE_TAGLINE = "Reserva Natural Comunitaria"
COMMUNITY_EMAIL = "lordmauricio22@gmail.com"
COMMUNITY_WHATSAPP = "+573188383917"
