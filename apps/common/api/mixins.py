"""Reusable API mixins."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from rest_framework import status
from rest_framework.response import Response

from apps.common.responses import APIResponse


class APIResponseMixin:
    """Provide consistent API response helpers."""

    request_id_header = "HTTP_X_REQUEST_ID"
    correlation_id_header = "HTTP_X_CORRELATION_ID"

    def get_response_meta(self) -> dict[str, str]:
        request = getattr(self, "request", None)
        if request is None:
            return {}

        meta = {}
        request_id = request.META.get(self.request_id_header)
        correlation_id = request.META.get(self.correlation_id_header)

        if request_id:
            meta["request_id"] = request_id
        if correlation_id:
            meta["correlation_id"] = correlation_id

        return meta

    def success_response(
        self,
        data: Any = None,
        *,
        status_code: int = status.HTTP_200_OK,
        meta: Mapping[str, Any] | None = None,
    ) -> Response:
        response_meta = self.get_response_meta()
        if meta:
            response_meta.update(meta)

        return APIResponse.success(
            data=data,
            status_code=status_code,
            meta=response_meta,
        )

    def error_response(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        details: Any = None,
        meta: Mapping[str, Any] | None = None,
    ) -> Response:
        response_meta = self.get_response_meta()
        if meta:
            response_meta.update(meta)

        return APIResponse.error(
            code=code,
            message=message,
            status_code=status_code,
            details=details,
            meta=response_meta,
        )
