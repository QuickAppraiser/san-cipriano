"""
Django local settings for San Cipriano project.
For running without Docker using SQLite.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "testserver"]

# SQLite database for local development without Docker
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Disable Redis cache - use local memory
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Email backend - use Gmail SMTP if configured, otherwise console
from decouple import config
_email_backend = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
if _email_backend == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_BACKEND = _email_backend
    EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="San Cipriano <noreply@sancipriano.co>")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS - Allow all in development
CORS_ALLOW_ALL_ORIGINS = True

# Static files
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Disable security settings for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Celery - run tasks synchronously in local dev
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Remove debug toolbar requirement
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]  # noqa: F405
MIDDLEWARE = [m for m in MIDDLEWARE if "debug_toolbar" not in m]  # noqa: F405
