"""Database configuration helpers."""

from __future__ import annotations

import dj_database_url

from .env import get_bool, get_int, get_str


def build_database_config() -> dict[str, dict[str, object]]:
    """Build the default database config from DATABASE_URL or POSTGRES_* values."""
    environment = get_str("DJANGO_ENVIRONMENT", "development")
    database_url = get_str("DATABASE_URL")
    conn_max_age = get_int(
        "POSTGRES_CONN_MAX_AGE",
        600 if environment == "production" else 60,
    )

    if database_url:
        ssl_require = get_bool(
            "POSTGRES_SSL_REQUIRE",
            environment == "production",
        )
        return {
            "default": dj_database_url.parse(
                database_url,
                conn_max_age=conn_max_age,
                ssl_require=ssl_require,
            )
        }

    return {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": get_str("POSTGRES_DB", "blogify"),
            "USER": get_str("POSTGRES_USER", "blogify"),
            "PASSWORD": get_str("POSTGRES_PASSWORD", "blogify"),
            "HOST": get_str("POSTGRES_HOST", "localhost"),
            "PORT": get_int("POSTGRES_PORT", 5432),
            "CONN_MAX_AGE": conn_max_age,
        }
    }
