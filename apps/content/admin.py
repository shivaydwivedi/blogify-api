"""Admin registration for content taxonomy models."""

from __future__ import annotations

from django.contrib import admin

from apps.content.models import Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for categories."""

    list_display = ("name", "slug", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "slug", "description")
    ordering = ("name",)
    readonly_fields = ("id", "slug", "created_at", "updated_at")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for tags."""

    list_display = ("name", "slug", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "slug")
    ordering = ("name",)
    readonly_fields = ("id", "slug", "created_at", "updated_at")
