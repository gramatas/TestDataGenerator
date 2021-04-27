"""Development settings."""

from .base import *  # NOQA
from .base import env

from datetime import timedelta

# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='1mhh4p(axq2b0+=ek7mh@=&g6dvr5v@vio4hl@a)5=l!e%e&ij')
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "*"
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025


# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405