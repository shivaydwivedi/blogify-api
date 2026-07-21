"""Centralized API error codes."""

from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    VALIDATION_ERROR = "validation_error"
    BUSINESS_RULE_VIOLATION = "business_rule_violation"
    PERMISSION_DENIED = "permission_denied"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    RATE_LIMITED = "rate_limited"
    AUTHENTICATION_FAILED = "authentication_failed"
    NOT_AUTHENTICATED = "not_authenticated"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    UNSUPPORTED_MEDIA_TYPE = "unsupported_media_type"
    PARSE_ERROR = "parse_error"
    SERVER_ERROR = "server_error"
