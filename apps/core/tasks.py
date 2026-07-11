"""Infrastructure tasks for verifying background processing."""

from __future__ import annotations

from datetime import UTC, datetime

from celery import shared_task


@shared_task(name="apps.core.tasks.background_ping")
def background_ping() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
    }
