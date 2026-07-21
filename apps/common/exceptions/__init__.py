"""Reusable exception framework."""

from apps.common.exceptions.codes import ErrorCode
from apps.common.exceptions.exceptions import (
    BaseAPIException,
    BusinessRuleException,
    ConflictException,
    PermissionDeniedException,
    RateLimitException,
    ResourceNotFoundException,
    ValidationException,
)
from apps.common.exceptions.handlers import global_exception_handler

__all__ = (
    "BaseAPIException",
    "BusinessRuleException",
    "ConflictException",
    "ErrorCode",
    "PermissionDeniedException",
    "RateLimitException",
    "ResourceNotFoundException",
    "ValidationException",
    "global_exception_handler",
)
