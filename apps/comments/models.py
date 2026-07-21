"""Comment domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.posts.models import Post


class Comment(BaseModel):
    """Comment or one-level reply on a published post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    content = models.TextField()
    is_edited = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        ordering = ("created_at",)
        indexes = (
            models.Index(fields=("post", "created_at")),
            models.Index(fields=("author", "created_at")),
        )
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.post}"
