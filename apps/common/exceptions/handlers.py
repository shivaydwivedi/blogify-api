"""Global DRF exception handler."""

from __future__ import annotations

import logging
from typing import Any

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
    Throttled,
    UnsupportedMediaType,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from apps.common.exceptions.codes import ErrorCode
from apps.common.exceptions.exceptions import BaseAPIException
from apps.common.exceptions.formatters import build_error_payload, get_request_meta

logger = logging.getLogger(__name__)


def global_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    request = context.get("request")
    meta = get_request_meta(request)

    if isinstance(exc, BaseAPIException):
        return Response(
            build_error_payload(
                code=exc.error_code,
                message=str(exc.client_message),
                details=exc.details,
                meta=meta,
            ),
            status=exc.status_code,
        )

    response = drf_exception_handler(exc, context)
    if response is not None:
        code, message, details = normalize_drf_exception(exc, response.data)
        response.data = build_error_payload(
            code=code,
            message=message,
            details=details,
            meta=meta,
        )
        return response

    logger.error(
        "Unhandled API exception",
        extra={
            "exception_type": exc.__class__.__name__,
            "request_meta": meta,
        },
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return Response(
        build_error_payload(
            code=ErrorCode.SERVER_ERROR.value,
            message="An unexpected error occurred.",
            meta=meta,
        ),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def normalize_drf_exception(
    exc: Exception,
    response_data: Any,
) -> tuple[str, str, Any]:
    if isinstance(exc, ValidationError):
        return ErrorCode.VALIDATION_ERROR.value, "Validation failed.", response_data
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return str(exc.get_codes()), str(exc.detail), []
    if isinstance(exc, PermissionDenied):
        return ErrorCode.PERMISSION_DENIED.value, str(exc.detail), []
    if isinstance(exc, (NotFound, Http404)):
        return ErrorCode.NOT_FOUND.value, "Resource not found.", []
    if isinstance(exc, MethodNotAllowed):
        return ErrorCode.METHOD_NOT_ALLOWED.value, str(exc.detail), []
    if isinstance(exc, UnsupportedMediaType):
        return ErrorCode.UNSUPPORTED_MEDIA_TYPE.value, str(exc.detail), []
    if isinstance(exc, ParseError):
        return ErrorCode.PARSE_ERROR.value, str(exc.detail), []
    if isinstance(exc, Throttled):
        return ErrorCode.RATE_LIMITED.value, str(exc.detail), []
    if isinstance(exc, APIException):
        return str(exc.get_codes()), str(exc.detail), []
    return ErrorCode.SERVER_ERROR.value, "An unexpected error occurred.", []
