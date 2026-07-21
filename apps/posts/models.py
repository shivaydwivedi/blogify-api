"""Post domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel
from apps.common.utils.slug import normalize_slug
from apps.common.utils.text import calculate_read_time_minutes
from apps.content.models import Category, Tag


class PostStatus(models.TextChoices):
    """Post publication states."""

    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class Post(BaseModel):
    """Blog post authored by a user."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="posts/", null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT,
        db_index=True,
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    reading_time = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = ("-created_at",)
        indexes = (
            models.Index(fields=("status", "published_at")),
            models.Index(fields=("author", "status")),
            models.Index(fields=("is_featured", "status")),
        )
        verbose_name = "post"
        verbose_name_plural = "posts"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = self.build_unique_slug()

        if self.status == PostStatus.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()

        self.reading_time = calculate_read_time_minutes(self.content)
        super().save(*args, **kwargs)

    def build_unique_slug(self) -> str:
        base_slug = normalize_slug(self.title, max_length=200)
        slug = base_slug
        suffix = 2

        while Post.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
            suffix_text = f"-{suffix}"
            slug = f"{base_slug[: 220 - len(suffix_text)]}{suffix_text}"
            suffix += 1

        return slug

    def __str__(self) -> str:
        return self.title
