"""Error response formatting helpers."""

from __future__ import annotations

from typing import Any

from apps.common.responses import APIResponse


def build_error_payload(
    *,
    code: str,
    message: str,
    details: Any = None,
    meta: dict[str, str] | None = None,
) -> dict[str, Any]:
    return APIResponse.error_payload(
        code=code,
        message=message,
        details=details,
        meta=meta,
    )


def get_request_meta(request: Any) -> dict[str, str]:
    if request is None:
        return {}

    meta = {}
    request_meta = getattr(request, "META", {})
    request_id = request_meta.get("HTTP_X_REQUEST_ID")
    correlation_id = request_meta.get("HTTP_X_CORRELATION_ID")

    if request_id:
        meta["request_id"] = request_id
    if correlation_id:
        meta["correlation_id"] = correlation_id

    return meta
