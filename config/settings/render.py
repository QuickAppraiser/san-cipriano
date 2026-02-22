"""
Django settings for Render.com deployment.
"""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-render-default-key")
DEBUG = False

ALLOWED_HOSTS = [
    ".onrender.com",
    "localhost",
    "127.0.0.1",
    "sanciprianoreserva.com",
    "www.sanciprianoreserva.com",
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third party
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    # Local apps
    "apps.core",
    "apps.visitors",
    "apps.content",
    "apps.notifications",
]

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

# Database - SQLite for free tier
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Check for DATABASE_URL (PostgreSQL)
import dj_database_url
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.config(default=DATABASE_URL, conn_max_age=600)

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

LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("it", "Italiano"),
    ("pt", "Português"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files - Simple configuration for Render
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise configuration for serving static files
# Using basic storage - WhiteNoise middleware will serve files from STATIC_ROOT
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache - local memory
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Security settings for HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False  # Render handles this
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://san-cipriano.onrender.com",
    "https://sanciprianoreserva.com",
    "https://www.sanciprianoreserva.com",
]

# CORS - Restringido a dominios específicos
CORS_ALLOWED_ORIGINS = [
    "https://san-cipriano.onrender.com",
    "https://sanciprianoreserva.com",
    "https://www.sanciprianoreserva.com",
]
CORS_ALLOW_ALL_ORIGINS = False

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Site settings
SITE_NAME = "San Cipriano"
SITE_TAGLINE = "Reserva Natural Comunitaria"
COMMUNITY_EMAIL = "lordmauricio22@gmail.com"
COMMUNITY_WHATSAPP = "+573188383917"
VISITOR_COUNTER_INITIAL = 45

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
