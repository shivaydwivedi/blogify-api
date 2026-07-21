"""Notification domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.comments.models import Comment
from apps.common.models import BaseModel
from apps.posts.models import Post


class NotificationType(models.TextChoices):
    """Supported notification event types."""

    EMAIL_VERIFIED = "email_verified", "Email Verified"
    POST_LIKED = "post_liked", "Post Liked"
    POST_COMMENTED = "post_commented", "Post Commented"
    COMMENT_REPLIED = "comment_replied", "Comment Replied"


class Notification(BaseModel):
    """User-facing notification."""

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="triggered_notifications",
    )
    type = models.CharField(max_length=40, choices=NotificationType.choices)
    title = models.CharField(max_length=160)
    message = models.TextField()
    related_post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    related_comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta(BaseModel.Meta):
        ordering = ("-created_at",)
        indexes = (
            models.Index(fields=("recipient", "is_read", "created_at")),
            models.Index(fields=("recipient", "type", "created_at")),
        )
        verbose_name = "notification"
        verbose_name_plural = "notifications"

    def __str__(self) -> str:
        return self.title
