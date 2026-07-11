"""Celery settings for asynchronous task processing."""

from __future__ import annotations

from datetime import timedelta

from .env import get_bool, get_int, get_str

REDIS_URL = get_str("REDIS_URL", "redis://localhost:6379/0")

CELERY_BROKER_URL = get_str("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = get_str("CELERY_RESULT_BACKEND", REDIS_URL)

CELERY_TASK_DEFAULT_QUEUE = get_str("CELERY_TASK_DEFAULT_QUEUE", "default")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = get_int("CELERY_TASK_TIME_LIMIT", 300)
CELERY_TASK_SOFT_TIME_LIMIT = get_int("CELERY_TASK_SOFT_TIME_LIMIT", 240)
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = get_int("CELERY_WORKER_PREFETCH_MULTIPLIER", 1)
CELERY_WORKER_SEND_TASK_EVENTS = get_bool("CELERY_WORKER_SEND_TASK_EVENTS", True)
CELERY_TASK_SEND_SENT_EVENT = get_bool("CELERY_TASK_SEND_SENT_EVENT", True)
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True
CELERY_RESULT_EXPIRES = get_int("CELERY_RESULT_EXPIRES", 3600)
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BEAT_SCHEDULE = {
    "core-background-ping": {
        "task": "apps.core.tasks.background_ping",
        "schedule": timedelta(minutes=5),
    },
}
