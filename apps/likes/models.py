"""Like domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import UUIDModel
from apps.posts.models import Post


class Like(UUIDModel):
    """A user's like on a post."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = (
            models.UniqueConstraint(
                fields=("user", "post"), name="unique_user_post_like"
            ),
        )
        indexes = (
            models.Index(fields=("post", "created_at")),
            models.Index(fields=("user", "created_at")),
        )
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self) -> str:
        return f"{self.user} liked {self.post}"
