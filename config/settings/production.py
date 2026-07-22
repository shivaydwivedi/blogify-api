"""Production settings for Blogify API."""

from __future__ import annotations

from .base import *  # noqa: F401,F403
from .env import (
    get_bool,
    get_int,
    get_list,
    get_str,
    reject_default_secret,
    require_env_vars,
)

DEBUG = False

require_env_vars(
    (
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
        "REDIS_URL",
        "CELERY_BROKER_URL",
        "CELERY_RESULT_BACKEND",
        "CLOUDINARY_URL",
        "EMAIL_HOST",
        "EMAIL_HOST_USER",
        "EMAIL_HOST_PASSWORD",
    )
)

if not get_str("DATABASE_URL"):
    require_env_vars(
        (
            "POSTGRES_DB",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_HOST",
            "POSTGRES_PORT",
        )
    )

SECRET_KEY = get_str("DJANGO_SECRET_KEY", required=True)
ALLOWED_HOSTS = get_list("DJANGO_ALLOWED_HOSTS", required=True)

reject_default_secret(SECRET_KEY)

STORAGES["default"] = {  # noqa: F405
    "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_str("EMAIL_HOST", required=True)
EMAIL_PORT = get_int("EMAIL_PORT", 587)
EMAIL_HOST_USER = get_str("EMAIL_HOST_USER", required=True)
EMAIL_HOST_PASSWORD = get_str("EMAIL_HOST_PASSWORD", required=True)
EMAIL_USE_TLS = get_bool("EMAIL_USE_TLS", True)
EMAIL_USE_SSL = get_bool("EMAIL_USE_SSL", False)

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = get_bool("DJANGO_SECURE_SSL_REDIRECT", True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = get_int("DJANGO_SECURE_HSTS_SECONDS", 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    True,
)
SECURE_HSTS_PRELOAD = get_bool("DJANGO_SECURE_HSTS_PRELOAD", True)
X_FRAME_OPTIONS = "DENY"
