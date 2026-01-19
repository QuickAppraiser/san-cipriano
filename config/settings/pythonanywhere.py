"""
Django settings for PythonAnywhere deployment.
San Cipriano - Turismo comunitario
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# PythonAnywhere domain
ALLOWED_HOSTS = [
    'sancipriano.pythonanywhere.com',
    'www.sancipriano.pythonanywhere.com',
]

# SQLite for PythonAnywhere free tier
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files - WhiteNoise handles this
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cache - Use database cache for free tier (no Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',
    }
}

# Disable Celery on free tier (no background workers)
CELERY_TASK_ALWAYS_EAGER = True

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS for PythonAnywhere
CORS_ALLOWED_ORIGINS = [
    'https://sancipriano.pythonanywhere.com',
]

# Email - Use console for testing, configure Resend/SendGrid for production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
