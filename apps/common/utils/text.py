"""Generic text helpers."""

from __future__ import annotations

import math
import re

from apps.common.utils.constants import DEFAULT_READ_TIME_WORDS_PER_MINUTE

WHITESPACE_PATTERN = re.compile(r"\s+")
WORD_PATTERN = re.compile(r"\b\w+\b")


def normalize_whitespace(value: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", value).strip()


def count_words(value: str) -> int:
    return len(WORD_PATTERN.findall(value))


def calculate_read_time_minutes(
    value: str,
    *,
    words_per_minute: int = DEFAULT_READ_TIME_WORDS_PER_MINUTE,
) -> int:
    if words_per_minute <= 0:
        raise ValueError("words_per_minute must be greater than zero.")

    word_count = count_words(value)
    if word_count == 0:
        return 0

    return max(1, math.ceil(word_count / words_per_minute))
