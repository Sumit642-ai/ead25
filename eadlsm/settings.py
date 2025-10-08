"""
Django settings for EADLSM project (production-friendly).

Notes:
- Reads sensitive values from environment variables (SECRET_KEY, DEBUG, DATABASE_URL, ALLOWED_HOSTS).
- Falls back to local SQLite if DATABASE_URL is not provided (so local dev works).
- Configures Whitenoise to serve static files (no extra setup required on Railway).
- STATICFILES_DIRS keeps your existing 'venues/static' and 'media' locations (update if your layout differs).
"""

import os
from pathlib import Path
import dj_database_url

# ---- Base paths ----
BASE_DIR = Path(__file__).resolve().parent.parent

# ---- Security & debug ----
# Read SECRET_KEY from env, fallback to an insecure local key (ONLY for dev).
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-fallback-replace-this-in-production"
)

# DEBUG should be 'True' or 'False' as a string env var. Default to False for safety.
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS: comma-separated env value, sensible defaults include localhost.
_default_hosts = "localhost,127.0.0.1"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", f"{_default_hosts}").split(",")

# ---- Installed apps ----
INSTALLED_APPS = [
    "venues",  # your app (keep it first if you rely on templates/static order)
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
    # Whitenoise for static file serving in production without extra webserver
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # keep if you use a project-level templates dir
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
# Use DATABASE_URL if provided (Railway / Heroku style). Fallback to local sqlite for dev.
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=False)
    }
else:
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
# static files collected into STATIC_ROOT by collectstatic
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Keep your current static dirs (update if your repo structure differs)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "venues", "static"),
    # add other static directories if needed
]

# Use compressed manifest storage to let Whitenoise serve compressed files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media (user-uploaded) files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ---- Default primary key field type ----
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---- Logging (simple, prints to stdout so PaaS captures it) ----
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

# ---- Extra dev-friendly settings ----
# Allow simple run of collectstatic even when DEBUG is True for local testing convenience.
# (No effect in production other than enabling collectstatic to populate staticfiles folder.)
