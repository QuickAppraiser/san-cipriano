"""
Django settings for Railway deployment.
"""

import os
import dj_database_url
from .base import *  # noqa: F401, F403

DEBUG = False

# Railway provides the RAILWAY_PUBLIC_DOMAIN environment variable
ALLOWED_HOSTS = [
    ".railway.app",
    "localhost",
    "127.0.0.1",
]

# Add the custom domain if set
RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)

# Database - Railway provides DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback to SQLite for initial deploy
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

# Static files with WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405

# Security settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
]

# Cache - use local memory for simplicity
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Email - console for now (can configure later)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Celery - run tasks synchronously
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

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
