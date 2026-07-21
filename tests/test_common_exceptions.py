from __future__ import annotations

from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.test import APIRequestFactory

from apps.common.exceptions import (
    BaseAPIException,
    BusinessRuleException,
    ConflictException,
    ErrorCode,
    PermissionDeniedException,
    RateLimitException,
    ResourceNotFoundException,
    ValidationException,
    global_exception_handler,
)


def build_context():
    request = APIRequestFactory().get(
        "/",
        HTTP_X_REQUEST_ID="request-123",
        HTTP_X_CORRELATION_ID="correlation-123",
    )
    return {"request": request}


def test_base_api_exception_carries_stable_error_contract() -> None:
    exc = BaseAPIException("Failure.", code="custom_error", details=[{"x": 1}])

    assert exc.error_code == "custom_error"
    assert exc.client_message == "Failure."
    assert exc.details == [{"x": 1}]


def test_project_exception_handler_returns_standard_error_envelope() -> None:
    response = global_exception_handler(
        ValidationException(details={"name": ["required"]}),
        build_context(),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "error": {
            "code": ErrorCode.VALIDATION_ERROR.value,
            "message": "Validation failed.",
            "details": {"name": ["required"]},
        },
        "meta": {
            "request_id": "request-123",
            "correlation_id": "correlation-123",
        },
    }


def test_framework_exception_status_codes() -> None:
    expected = {
        BusinessRuleException: status.HTTP_422_UNPROCESSABLE_ENTITY,
        PermissionDeniedException: status.HTTP_403_FORBIDDEN,
        ResourceNotFoundException: status.HTTP_404_NOT_FOUND,
        ConflictException: status.HTTP_409_CONFLICT,
        RateLimitException: status.HTTP_429_TOO_MANY_REQUESTS,
    }

    for exception_class, status_code in expected.items():
        response = global_exception_handler(exception_class(), build_context())

        assert response.status_code == status_code


def test_drf_validation_error_is_normalized() -> None:
    response = global_exception_handler(
        ValidationError({"name": ["This field is required."]}),
        build_context(),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert response.data["error"]["message"] == "Validation failed."
    assert response.data["error"]["details"] == {"name": ["This field is required."]}


def test_drf_authentication_error_is_normalized() -> None:
    response = global_exception_handler(NotAuthenticated(), build_context())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == ErrorCode.NOT_AUTHENTICATED.value
    assert response.data["error"]["details"] == []


def test_unhandled_exception_is_logged_and_safely_normalized(monkeypatch) -> None:
    captured = {}

    def capture_error(message, **kwargs):
        captured["message"] = message
        captured["kwargs"] = kwargs

    monkeypatch.setattr(
        "apps.common.exceptions.handlers.logger.error",
        capture_error,
    )

    response = global_exception_handler(RuntimeError("boom"), build_context())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["error"] == {
        "code": ErrorCode.SERVER_ERROR.value,
        "message": "An unexpected error occurred.",
        "details": [],
    }
    assert captured["message"] == "Unhandled API exception"
    assert captured["kwargs"]["extra"]["exception_type"] == "RuntimeError"
