"""Admin registration for comments."""

from __future__ import annotations

from django.contrib import admin

from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for comments."""

    list_display = ("post", "author", "parent", "is_edited", "created_at")
    list_filter = ("is_edited", "created_at", "updated_at")
    search_fields = ("content", "post__title", "author__email", "author__username")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
