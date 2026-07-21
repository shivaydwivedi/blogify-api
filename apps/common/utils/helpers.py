"""Small generic helper functions."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

T = TypeVar("T")


def is_blank(value: str | None) -> bool:
    return value is None or value.strip() == ""


def compact_dict(value: Mapping[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if item is not None}


def flatten(values: Iterable[Iterable[T]]) -> list[T]:
    return [item for group in values for item in group]
