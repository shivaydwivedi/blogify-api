"""Generic slug helpers."""

from __future__ import annotations

from django.utils.text import slugify

from apps.common.utils.constants import MAX_SLUG_LENGTH
from apps.common.utils.validators import validate_slug


def normalize_slug(value: str, *, max_length: int = MAX_SLUG_LENGTH) -> str:
    slug = slugify(value).strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].strip("-")

    validate_slug(slug, max_length=max_length)
    return slug
