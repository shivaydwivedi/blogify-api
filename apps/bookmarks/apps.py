"""Application configuration for bookmarks."""

from __future__ import annotations

from django.apps import AppConfig


class BookmarksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bookmarks"
    verbose_name = "Bookmarks"
