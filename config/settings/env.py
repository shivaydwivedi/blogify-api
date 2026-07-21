"""Environment loading and validation helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR: Final = Path(__file__).resolve().parents[2]
ENV_FILE: Final = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

TRUE_VALUES: Final = {"1", "true", "yes", "on"}
FALSE_VALUES: Final = {"0", "false", "no", "off"}


def get_str(name: str, default: str | None = None, *, required: bool = False) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        if required:
            raise ImproperlyConfigured(f"Missing required environment variable: {name}")
        if default is None:
            return ""
        return default
    return value


def get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None or value == "":
        return default

    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False

    raise ImproperlyConfigured(f"Environment variable {name} must be a boolean value.")


def get_int(name: str, default: int | None = None, *, required: bool = False) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        if required:
            raise ImproperlyConfigured(f"Missing required environment variable: {name}")
        if default is None:
            return 0
        return default

    try:
        return int(value)
    except ValueError as exc:
        raise ImproperlyConfigured(
            f"Environment variable {name} must be an integer."
        ) from exc


def get_list(
    name: str,
    default: tuple[str, ...] = (),
    *,
    required: bool = False,
) -> list[str]:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        if required:
            raise ImproperlyConfigured(f"Missing required environment variable: {name}")
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


def require_env_vars(names: tuple[str, ...]) -> None:
    missing = [name for name in names if os.getenv(name) in {None, ""}]
    if missing:
        joined = ", ".join(sorted(missing))
        raise ImproperlyConfigured(f"Missing required environment variables: {joined}")


def reject_default_secret(secret_key: str) -> None:
    unsafe_values = {
        "change-me-in-development",
        "unsafe-development-secret-key",
        "unsafe-development-secret-key-change-me",
    }
    if secret_key in unsafe_values:
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be changed for production.")
