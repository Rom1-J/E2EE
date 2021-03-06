import pygments.formatters

from .base import *  # noqa
from .base import env

# GENERAL
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="1NNX7lxXh2TyzoKqDwB7RKTDpi05hDXTl2hq4ew53nm8OabK8OaoVSLOu7qsZsiw",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "192.168.1.21"]
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS.copy()

# CACHES
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025

# WhiteNoise
# -----------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic"
] + INSTALLED_APPS  # noqa F405

# django-debug-toolbar
# -----------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# django-extensions
# -----------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# Your stuff...
ACCOUNT_ALLOW_REGISTRATION = True
SHELL_PLUS = "bpython"

SHELL_PLUS_PRINT_SQL = True

# Truncate sql queries to this number of characters (this is the default)
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

# Specify sqlparse configuration options when printing sql queries to the console
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
    reindent_aligned=True,
    truncate_strings=500,
)

# Specify Pygments formatter and configuration options when printing sql queries to the console
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}

if not DEBUG:
    # -------------------------------------------------------------------------
    # django-compressor
    # -------------------------------------------------------------------------
    # https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
    COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
    # https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
    COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
    # https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
    COMPRESS_URL = STATIC_URL  # noqa F405
    # https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
    COMPRESS_OFFLINE = (
        True  # Offline compression is required when using Whitenoise
    )
    # https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_FILTERS
    COMPRESS_FILTERS = {
        "css": [
            "compressor.filters.css_default.CssAbsoluteFilter",
            "compressor.filters.cssmin.rCSSMinFilter",
        ],
        "js": ["compressor.filters.jsmin.JSMinFilter"],
    }
