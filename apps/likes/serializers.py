"""Serializers for like APIs."""

from __future__ import annotations

from rest_framework import serializers

from apps.likes.models import Like
from apps.posts.serializers import AuthorSerializer


class LikeSerializer(serializers.ModelSerializer):
    """Serialize post likes."""

    user = AuthorSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "post", "created_at")
        read_only_fields = fields
