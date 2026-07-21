from __future__ import annotations

from datetime import UTC, datetime, timezone

import pytest
from django.core.exceptions import ValidationError

from apps.common.utils import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    SortDirection,
    calculate_read_time_minutes,
    compact_dict,
    ensure_aware_utc,
    flatten,
    format_iso_utc,
    is_blank,
    normalize_slug,
    normalize_whitespace,
    now_utc,
    validate_page_size,
    validate_slug,
)
from apps.common.utils.text import count_words


def test_constants_match_api_contract() -> None:
    assert DEFAULT_PAGE_SIZE == 20
    assert MAX_PAGE_SIZE == 100


def test_sort_direction_values_are_stable() -> None:
    assert SortDirection.ASCENDING.value == "asc"
    assert SortDirection.DESCENDING.value == "desc"


def test_normalize_slug_creates_url_safe_slug() -> None:
    assert normalize_slug(" Hello, Blogify API! ") == "hello-blogify-api"


def test_validate_slug_rejects_invalid_slug() -> None:
    with pytest.raises(ValidationError):
        validate_slug("Invalid Slug")


def test_validate_page_size_accepts_valid_size() -> None:
    assert validate_page_size(25) == 25


@pytest.mark.parametrize("value", [0, 101])
def test_validate_page_size_rejects_invalid_size(value) -> None:
    with pytest.raises(ValidationError):
        validate_page_size(value)


def test_normalize_whitespace_compacts_text() -> None:
    assert normalize_whitespace("hello\n\n  world") == "hello world"


def test_count_words_counts_text_words() -> None:
    assert count_words("hello, world") == 2


def test_calculate_read_time_minutes_rounds_up() -> None:
    text = "word " * 201

    assert calculate_read_time_minutes(text, words_per_minute=200) == 2


def test_calculate_read_time_minutes_handles_empty_text() -> None:
    assert calculate_read_time_minutes("") == 0


def test_calculate_read_time_minutes_rejects_invalid_rate() -> None:
    with pytest.raises(ValueError):
        calculate_read_time_minutes("hello", words_per_minute=0)


def test_now_utc_returns_aware_utc_datetime() -> None:
    value = now_utc()

    assert value.tzinfo == UTC


def test_ensure_aware_utc_converts_naive_datetime() -> None:
    value = ensure_aware_utc(datetime(2026, 1, 1, 12, 0, 0))

    assert value.tzinfo == UTC


def test_ensure_aware_utc_converts_aware_datetime() -> None:
    source = datetime(2026, 1, 1, 17, 30, 0, tzinfo=timezone.utc)

    assert ensure_aware_utc(source).tzinfo == UTC


def test_format_iso_utc_returns_iso_string() -> None:
    value = format_iso_utc(datetime(2026, 1, 1, 12, 0, 0))

    assert value == "2026-01-01T12:00:00+00:00"


def test_is_blank_detects_empty_text() -> None:
    assert is_blank(None) is True
    assert is_blank("   ") is True
    assert is_blank("value") is False


def test_compact_dict_removes_none_values() -> None:
    assert compact_dict({"a": 1, "b": None, "c": 0}) == {"a": 1, "c": 0}


def test_flatten_combines_nested_iterables() -> None:
    assert flatten([[1, 2], [3]]) == [1, 2, 3]
