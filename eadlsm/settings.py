"""
Production-friendly Django settings for prototype (SQLite fallback).

This settings file intentionally avoids any external DB connection (Postgres)
and uses SQLite so deployments on Railway won't fail due to unreachable DB hosts.
Note: SQLite on PaaS is ephemeral — good for prototypes, not for production data.
"""

import os
from pathlib import Path

# ---- Base paths ----
BASE_DIR = Path(__file__).resolve().parent.parent

# ---- Security & debug ----
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-fallback-replace-this-in-production"
)

# Default to False in production; set DEBUG=True locally if you want.
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS: allow Railway default host plus localhost. You can update via env var if needed.
_default_hosts = "localhost,127.0.0.1"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", f"{_default_hosts}").split(",")

# ---- Installed apps ----
INSTALLED_APPS = [
    "venues",  # your app (keep it here if your app is named 'venues')
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ---- Middleware ----
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---- URL / WSGI ----
ROOT_URLCONF = "eadlsm.urls"
WSGI_APPLICATION = "eadlsm.wsgi.application"
ASGI_APPLICATION = "eadlsm.asgi.application"

# ---- Templates ----
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---- Database ----
# PROTOTYPE MODE: Force SQLite to avoid external DB connectivity issues on PaaS.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# ---- Password validation ----
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---- Internationalization ----
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# ---- Static & media files ----
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "venues", "static"),
    # Add any other static dirs you have here
]

# Whitenoise storage for compressed static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ---- Default primary key field type ----
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---- Logging ----
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ---- Convenience: print a short warning when DEBUG=False and using SQLite ----
if not DEBUG:
    import warnings

    warnings.warn(
        "Running with DEBUG=False and using SQLite (ephemeral). "
        "This is OK for prototypes but not for production databases."
    )
