"""Generic test helper functions."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def merge_dicts(*values: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for value in values:
        merged.update(value)
    return merged


def build_response_meta(
    *,
    request_id: str | None = None,
    correlation_id: str | None = None,
) -> dict[str, str]:
    meta = {}
    if request_id:
        meta["request_id"] = request_id
    if correlation_id:
        meta["correlation_id"] = correlation_id
    return meta
