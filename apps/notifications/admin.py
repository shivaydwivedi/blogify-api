"""Admin registration for notifications."""

from __future__ import annotations

from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin configuration for notifications."""

    list_display = ("recipient", "type", "title", "is_read", "created_at")
    list_filter = ("recipient", "type", "is_read", "created_at")
    search_fields = ("recipient__email", "actor__email", "title", "message")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
