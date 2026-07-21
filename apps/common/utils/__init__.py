"""Reusable utility framework."""

from apps.common.utils.constants import (
    DEFAULT_PAGE_SIZE,
    DEFAULT_READ_TIME_WORDS_PER_MINUTE,
    MAX_PAGE_SIZE,
    MAX_SLUG_LENGTH,
)
from apps.common.utils.datetime import ensure_aware_utc, format_iso_utc, now_utc
from apps.common.utils.enums import SortDirection
from apps.common.utils.helpers import compact_dict, flatten, is_blank
from apps.common.utils.slug import normalize_slug
from apps.common.utils.text import calculate_read_time_minutes, normalize_whitespace
from apps.common.utils.validators import validate_page_size, validate_slug

__all__ = (
    "DEFAULT_PAGE_SIZE",
    "DEFAULT_READ_TIME_WORDS_PER_MINUTE",
    "MAX_PAGE_SIZE",
    "MAX_SLUG_LENGTH",
    "SortDirection",
    "calculate_read_time_minutes",
    "compact_dict",
    "ensure_aware_utc",
    "flatten",
    "format_iso_utc",
    "is_blank",
    "normalize_slug",
    "normalize_whitespace",
    "now_utc",
    "validate_page_size",
    "validate_slug",
)
