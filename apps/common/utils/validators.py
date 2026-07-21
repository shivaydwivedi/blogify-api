"""Generic validation helpers."""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError

from apps.common.utils.constants import MAX_PAGE_SIZE, MAX_SLUG_LENGTH

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_slug(value: str, *, max_length: int = MAX_SLUG_LENGTH) -> str:
    if len(value) > max_length:
        raise ValidationError(f"Slug must be at most {max_length} characters.")

    if not SLUG_PATTERN.fullmatch(value):
        raise ValidationError(
            "Slug may contain lowercase letters, numbers, and single hyphens."
        )

    return value


def validate_page_size(value: int, *, max_page_size: int = MAX_PAGE_SIZE) -> int:
    if value < 1:
        raise ValidationError("Page size must be greater than zero.")

    if value > max_page_size:
        raise ValidationError(f"Page size must not exceed {max_page_size}.")

    return value
