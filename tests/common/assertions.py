"""Reusable response assertion helpers."""

from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.response import Response


class ResponseAssertions:
    """Assertions for the approved API response envelope."""

    def assert_success_response(
        self,
        response: Response,
        *,
        data: Any = None,
        status_code: int = status.HTTP_200_OK,
        meta: dict[str, Any] | None = None,
    ) -> None:
        assert response.status_code == status_code
        expected: dict[str, Any] = {"data": data}
        if meta:
            expected["meta"] = meta
        assert response.data == expected

    def assert_created_response(
        self,
        response: Response,
        *,
        data: Any = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        self.assert_success_response(
            response,
            data=data,
            status_code=status.HTTP_201_CREATED,
            meta=meta,
        )

    def assert_empty_response(
        self,
        response: Response,
        *,
        status_code: int = status.HTTP_204_NO_CONTENT,
    ) -> None:
        assert response.status_code == status_code
        assert response.data is None

    def assert_error_response(
        self,
        response: Response,
        *,
        code: str,
        message: str,
        status_code: int,
        details: Any = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        assert response.status_code == status_code
        expected: dict[str, Any] = {
            "error": {
                "code": code,
                "message": message,
                "details": [] if details is None else details,
            },
        }
        if meta:
            expected["meta"] = meta
        assert response.data == expected

    def assert_paginated_response(
        self,
        response: Response,
        *,
        data: Any,
        pagination: dict[str, Any],
        meta: dict[str, Any] | None = None,
    ) -> None:
        assert response.status_code == status.HTTP_200_OK
        expected: dict[str, Any] = {
            "data": data,
            "pagination": pagination,
        }
        if meta:
            expected["meta"] = meta
        assert response.data == expected

    def assert_validation_error(
        self,
        response: Response,
        *,
        details: Any,
        message: str = "Validation failed.",
    ) -> None:
        self.assert_error_response(
            response,
            code="validation_error",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )
