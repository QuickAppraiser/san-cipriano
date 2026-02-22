"""
Django base settings for San Cipriano project.
Sitio web oficial de la comunidad de San Cipriano, Colombia.
Turismo comunitario, conservación ambiental y control responsable de visitantes.
"""

import os
from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_extensions",
    "modeltranslation",
    "drf_spectacular",
    "django_celery_beat",
    "anymail",
]

LOCAL_APPS = [
    "apps.core",
    "apps.visitors",
    "apps.content",
    "apps.notifications",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="san_cipriano"),
        "USER": config("POSTGRES_USER", default="postgres"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="postgres"),
        "HOST": config("POSTGRES_HOST", default="localhost"),
        "PORT": config("POSTGRES_PORT", default="5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("it", "Italiano"),
    ("pt", "Português"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# Modeltranslation settings
MODELTRANSLATION_DEFAULT_LANGUAGE = "es"
MODELTRANSLATION_LANGUAGES = ("es", "en", "fr", "de", "it", "pt")

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (User uploaded)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# DRF Spectacular (API Documentation)
SPECTACULAR_SETTINGS = {
    "TITLE": "San Cipriano API",
    "DESCRIPTION": "API para el sitio web oficial de la comunidad de San Cipriano",
    "VERSION": "1.0.0",
}

# Redis & Caching
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery Configuration
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default=REDIS_URL)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Email Configuration
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="San Cipriano <noreply@sancipriano.co>")

# Anymail (for production email services)
ANYMAIL = {
    "RESEND_API_KEY": config("RESEND_API_KEY", default=""),
}

# WhatsApp Configuration
WHATSAPP_API_URL = config("WHATSAPP_API_URL", default="")
WHATSAPP_API_TOKEN = config("WHATSAPP_API_TOKEN", default="")
WHATSAPP_PHONE_ID = config("WHATSAPP_PHONE_ID", default="")
WHATSAPP_COMMUNITY_NUMBER = config("WHATSAPP_COMMUNITY_NUMBER", default="+573188383917")

# Site Configuration
SITE_NAME = "San Cipriano"
SITE_TAGLINE = "Reserva Natural Comunitaria"
COMMUNITY_EMAIL = config("COMMUNITY_EMAIL", default="lordmauricio22@gmail.com")
COMMUNITY_WHATSAPP = config("COMMUNITY_WHATSAPP", default="+573188383917")

# Visitor Counter Initial Value
VISITOR_COUNTER_INITIAL = config("VISITOR_COUNTER_INITIAL", default=180, cast=int)

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# CORS Settings
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:8000,http://127.0.0.1:8000",
    cast=Csv()
)

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": config("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
