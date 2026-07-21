"""Serializers for content taxonomy APIs."""

from __future__ import annotations

from rest_framework import serializers

from apps.content.models import Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """Serialize category resources."""

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def validate_name(self, value: str) -> str:
        queryset = Category.all_objects.filter(name__iexact=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A category with this name already exists."
            )

        return value


class TagSerializer(serializers.ModelSerializer):
    """Serialize tag resources."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "slug",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def validate_name(self, value: str) -> str:
        queryset = Tag.all_objects.filter(name__iexact=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A tag with this name already exists.")

        return value
