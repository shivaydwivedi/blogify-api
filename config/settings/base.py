"""Base Django settings for Blogify API."""

from __future__ import annotations

from . import celery as celery_settings
from . import rest_framework as drf_settings
from . import simple_jwt as simple_jwt_settings
from . import spectacular as spectacular_settings
from .env import BASE_DIR, get_bool, get_int, get_list, get_str
from .logging import build_logging_config

ENVIRONMENT = get_str("DJANGO_ENVIRONMENT", "development")
SECRET_KEY = get_str(
    "DJANGO_SECRET_KEY",
    "unsafe-development-secret-key-change-me",
)
DEBUG = get_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = get_list("DJANGO_ALLOWED_HOSTS", ("localhost", "127.0.0.1"))
CSRF_TRUSTED_ORIGINS = get_list("DJANGO_CSRF_TRUSTED_ORIGINS")

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "rest_framework_simplejwt.token_blacklist",
    "apps.accounts",
    "apps.common",
    "apps.content",
    "apps.posts",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

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
            ],
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_str("POSTGRES_DB", "blogify"),
        "USER": get_str("POSTGRES_USER", "blogify"),
        "PASSWORD": get_str("POSTGRES_PASSWORD", "blogify"),
        "HOST": get_str("POSTGRES_HOST", "localhost"),
        "PORT": get_int("POSTGRES_PORT", 5432),
        "CONN_MAX_AGE": get_int("POSTGRES_CONN_MAX_AGE", 60),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = drf_settings.REST_FRAMEWORK
SIMPLE_JWT = simple_jwt_settings.SIMPLE_JWT
SPECTACULAR_SETTINGS = spectacular_settings.SPECTACULAR_SETTINGS
LOGGING = build_logging_config(BASE_DIR)

REDIS_URL = celery_settings.REDIS_URL
CELERY_BROKER_URL = celery_settings.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = celery_settings.CELERY_RESULT_BACKEND
CELERY_TASK_DEFAULT_QUEUE = celery_settings.CELERY_TASK_DEFAULT_QUEUE
CELERY_TASK_TRACK_STARTED = celery_settings.CELERY_TASK_TRACK_STARTED
CELERY_TASK_TIME_LIMIT = celery_settings.CELERY_TASK_TIME_LIMIT
CELERY_TASK_SOFT_TIME_LIMIT = celery_settings.CELERY_TASK_SOFT_TIME_LIMIT
CELERY_TASK_ACKS_LATE = celery_settings.CELERY_TASK_ACKS_LATE
CELERY_TASK_REJECT_ON_WORKER_LOST = celery_settings.CELERY_TASK_REJECT_ON_WORKER_LOST
CELERY_WORKER_PREFETCH_MULTIPLIER = celery_settings.CELERY_WORKER_PREFETCH_MULTIPLIER
CELERY_WORKER_SEND_TASK_EVENTS = celery_settings.CELERY_WORKER_SEND_TASK_EVENTS
CELERY_TASK_SEND_SENT_EVENT = celery_settings.CELERY_TASK_SEND_SENT_EVENT
CELERY_TIMEZONE = celery_settings.CELERY_TIMEZONE
CELERY_ENABLE_UTC = celery_settings.CELERY_ENABLE_UTC
CELERY_RESULT_EXPIRES = celery_settings.CELERY_RESULT_EXPIRES
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = (
    celery_settings.CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP
)
CELERY_BEAT_SCHEDULE = celery_settings.CELERY_BEAT_SCHEDULE
