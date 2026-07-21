"""Filters for post APIs."""

from __future__ import annotations

import django_filters

from apps.common.api import BaseFilter
from apps.posts.models import Post


class PostFilter(BaseFilter):
    """Explicit filters supported by the post collection."""

    category = django_filters.UUIDFilter(field_name="category_id")
    tag = django_filters.UUIDFilter(field_name="tags__id")
    author = django_filters.UUIDFilter(field_name="author_id")
    featured = django_filters.BooleanFilter(field_name="is_featured")

    class Meta:
        model = Post
        fields = ("category", "tag", "author", "status", "featured")
