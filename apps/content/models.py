"""Content taxonomy models."""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseModel
from apps.common.utils.slug import normalize_slug


class Category(BaseModel):
    """Category used to organize posts."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta(BaseModel.Meta):
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = normalize_slug(self.name, max_length=100)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Tag(BaseModel):
    """Tag used for flexible post labeling."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta(BaseModel.Meta):
        ordering = ("name",)
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = normalize_slug(self.name, max_length=100)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
