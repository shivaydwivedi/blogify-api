"""Canonical API response builders."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """Build API responses using the approved response envelope."""

    @staticmethod
    def success(
        data: Any = None,
        *,
        status_code: int = status.HTTP_200_OK,
        meta: Mapping[str, Any] | None = None,
    ) -> Response:
        return Response(
            APIResponse.success_payload(data=data, meta=meta),
            status=status_code,
        )

    @staticmethod
    def created(
        data: Any = None,
        *,
        meta: Mapping[str, Any] | None = None,
    ) -> Response:
        return APIResponse.success(
            data=data,
            status_code=status.HTTP_201_CREATED,
            meta=meta,
        )

    @staticmethod
    def updated(
        data: Any = None,
        *,
        meta: Mapping[str, Any] | None = None,
    ) -> Response:
        return APIResponse.success(data=data, meta=meta)

    @staticmethod
    def deleted() -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def empty(
        *,
        status_code: int = status.HTTP_204_NO_CONTENT,
    ) -> Response:
        return Response(status=status_code)

    @staticmethod
    def paginated(
        *,
        data: Any,
        pagination: Mapping[str, Any],
        meta: Mapping[str, Any] | None = None,
    ) -> Response:
        payload = APIResponse.paginated_payload(
            data=data,
            pagination=pagination,
            meta=meta,
        )
        return Response(payload, status=status.HTTP_200_OK)

    @staticmethod
    def error(
        *,
        code: str,
        message: str,
        status_code: int,
        details: Any = None,
        meta: Mapping[str, Any] | None = None,
    ) -> Response:
        return Response(
            APIResponse.error_payload(
                code=code,
                message=message,
                details=details,
                meta=meta,
            ),
            status=status_code,
        )

    @staticmethod
    def success_payload(
        *,
        data: Any = None,
        meta: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"data": data}
        if meta:
            payload["meta"] = dict(meta)
        return payload

    @staticmethod
    def paginated_payload(
        *,
        data: Any,
        pagination: Mapping[str, Any],
        meta: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "data": data,
            "pagination": dict(pagination),
        }
        if meta:
            payload["meta"] = dict(meta)
        return payload

    @staticmethod
    def error_payload(
        *,
        code: str,
        message: str,
        details: Any = None,
        meta: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "error": {
                "code": code,
                "message": message,
                "details": [] if details is None else details,
            },
        }
        if meta:
            payload["meta"] = dict(meta)
        return payload
