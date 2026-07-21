"""Admin registration for likes."""

from __future__ import annotations

from django.contrib import admin

from apps.likes.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin configuration for likes."""

    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "user__username", "post__title")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at")
