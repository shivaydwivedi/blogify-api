"""Admin registration for post domain models."""

from __future__ import annotations

from django.contrib import admin

from apps.posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for posts."""

    list_display = (
        "title",
        "author",
        "category",
        "status",
        "is_featured",
        "published_at",
        "created_at",
    )
    list_filter = ("status", "is_featured", "category", "created_at", "published_at")
    search_fields = ("title", "slug", "excerpt", "content", "author__email")
    ordering = ("-created_at",)
    readonly_fields = (
        "id",
        "slug",
        "reading_time",
        "view_count",
        "published_at",
        "created_at",
        "updated_at",
    )
    filter_horizontal = ("tags",)
