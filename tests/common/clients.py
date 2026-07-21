"""Reusable API client helpers."""

from __future__ import annotations

from typing import Any

from rest_framework.test import APIClient


def build_request_headers(
    *,
    request_id: str | None = None,
    correlation_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = dict(extra or {})
    if request_id:
        headers["HTTP_X_REQUEST_ID"] = request_id
    if correlation_id:
        headers["HTTP_X_CORRELATION_ID"] = correlation_id
    return headers


def build_api_client(*, headers: dict[str, Any] | None = None) -> APIClient:
    client = APIClient()
    if headers:
        client.defaults.update(headers)
    return client
