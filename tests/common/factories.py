"""Generic factory foundations for test data."""

from __future__ import annotations

from itertools import count
from typing import Any, ClassVar


class BaseFactory:
    """Build dictionary-based test data without feature coupling."""

    sequence_start: ClassVar[int] = 1
    _sequence: ClassVar[count] = count(sequence_start)

    @classmethod
    def next_sequence(cls) -> int:
        return next(cls._sequence)

    @classmethod
    def reset_sequence(cls, value: int | None = None) -> None:
        cls._sequence = count(cls.sequence_start if value is None else value)

    @classmethod
    def defaults(cls) -> dict[str, Any]:
        return {}

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        attributes = cls.defaults()
        attributes.update(overrides)
        return attributes

    @classmethod
    def build_batch(cls, size: int, **overrides: Any) -> list[dict[str, Any]]:
        return [cls.build(**overrides) for _ in range(size)]
