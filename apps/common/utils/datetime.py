"""Timezone-aware datetime helpers."""

from __future__ import annotations

from datetime import UTC, datetime


def now_utc() -> datetime:
    return datetime.now(UTC)


def ensure_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def format_iso_utc(value: datetime) -> str:
    return ensure_aware_utc(value).isoformat()
