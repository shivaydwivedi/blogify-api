"""Production settings for Blogify API."""

from __future__ import annotations

from .base import *  # noqa: F401,F403
from .env import get_list, get_str, reject_default_secret, require_env_vars

DEBUG = False

require_env_vars(
    (
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
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

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
