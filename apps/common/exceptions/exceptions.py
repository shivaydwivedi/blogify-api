"""Reusable client-facing API exceptions."""

from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.exceptions import APIException

from apps.common.exceptions.codes import ErrorCode


class BaseAPIException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An unexpected error occurred."
    default_code = ErrorCode.SERVER_ERROR.value

    def __init__(
        self,
        detail: Any = None,
        *,
        code: str | ErrorCode | None = None,
        details: Any = None,
        status_code: int | None = None,
    ) -> None:
        self.client_message = detail or self.default_detail
        self.error_code = str(code or self.default_code)
        self.details = [] if details is None else details
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=self.client_message, code=self.error_code)


class ValidationException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Validation failed."
    default_code = ErrorCode.VALIDATION_ERROR.value


class BusinessRuleException(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "The request violates a business rule."
    default_code = ErrorCode.BUSINESS_RULE_VIOLATION.value


class PermissionDeniedException(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Permission denied."
    default_code = ErrorCode.PERMISSION_DENIED.value


class ResourceNotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found."
    default_code = ErrorCode.NOT_FOUND.value


class ConflictException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "The request conflicts with the current resource state."
    default_code = ErrorCode.CONFLICT.value


class RateLimitException(BaseAPIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = "Rate limit exceeded."
    default_code = ErrorCode.RATE_LIMITED.value
