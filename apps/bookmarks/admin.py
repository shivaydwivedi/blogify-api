"""Admin registration for bookmarks."""

from __future__ import annotations

from django.contrib import admin

from apps.bookmarks.models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Admin configuration for bookmarks."""

    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "user__username", "post__title")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at")
