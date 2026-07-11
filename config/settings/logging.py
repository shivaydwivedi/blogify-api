"""Logging configuration for Blogify API."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .env import get_bool, get_str


def build_logging_config(base_dir: Path) -> dict[str, Any]:
    log_level = get_str("DJANGO_LOG_LEVEL", "INFO").upper()
    enable_file_logging = get_bool("DJANGO_ENABLE_FILE_LOGGING", False)

    handlers: dict[str, dict[str, Any]] = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "structured",
        },
    }
    active_handlers = ["console"]

    if enable_file_logging:
        log_file_path = Path(
            get_str("DJANGO_LOG_FILE_PATH", str(base_dir / "logs" / "blogify.log"))
        )
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "structured",
            "filename": str(log_file_path),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
        }
        active_handlers.append("file")

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": {
                "format": (
                    "timestamp=%(asctime)s level=%(levelname)s "
                    "logger=%(name)s module=%(module)s message=%(message)s"
                ),
            },
        },
        "handlers": handlers,
        "root": {
            "handlers": active_handlers,
            "level": log_level,
        },
        "loggers": {
            "django": {
                "handlers": active_handlers,
                "level": log_level,
                "propagate": False,
            },
            "apps": {
                "handlers": active_handlers,
                "level": log_level,
                "propagate": False,
            },
            "config": {
                "handlers": active_handlers,
                "level": log_level,
                "propagate": False,
            },
            "blogify.security": {
                "handlers": active_handlers,
                "level": get_str("DJANGO_SECURITY_LOG_LEVEL", "INFO").upper(),
                "propagate": False,
            },
        },
    }
