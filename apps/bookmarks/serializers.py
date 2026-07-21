"""Serializers for bookmark APIs."""

from __future__ import annotations

from rest_framework import serializers

from apps.bookmarks.models import Bookmark
from apps.posts.serializers import PostListSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    """Serialize user bookmarks."""

    post = PostListSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ("id", "post", "created_at")
        read_only_fields = fields
