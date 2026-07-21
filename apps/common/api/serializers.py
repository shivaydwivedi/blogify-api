"""Reusable serializer foundations."""

from __future__ import annotations

from typing import Any

from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Base serializer for request and response boundary objects."""

    server_controlled_fields: tuple[str, ...] = ()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        for field_name in self.server_controlled_fields:
            attrs.pop(field_name, None)
        return super().validate(attrs)
