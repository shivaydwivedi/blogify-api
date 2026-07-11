"""Celery application configuration for Blogify API."""

from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("blogify")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
