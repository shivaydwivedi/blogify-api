"""Serializers for notification APIs."""

from __future__ import annotations

from rest_framework import serializers

from apps.notifications.models import Notification
from apps.posts.serializers import AuthorSerializer, PostListSerializer


class NotificationListSerializer(serializers.ModelSerializer):
    """Serialize notifications for the owner."""

    actor = AuthorSerializer(read_only=True)
    related_post = PostListSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "recipient",
            "actor",
            "type",
            "title",
            "message",
            "related_post",
            "related_comment",
            "is_read",
            "created_at",
        )
        read_only_fields = fields


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Schema marker for notification read actions."""

    class Meta:
        model = Notification
        fields = ("is_read",)
        read_only_fields = ("is_read",)
