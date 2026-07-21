"""Shared enum primitives."""

from __future__ import annotations

from enum import StrEnum


class SortDirection(StrEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"
