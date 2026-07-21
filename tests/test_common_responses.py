from __future__ import annotations

from rest_framework import status

from apps.common.responses import APIResponse


def test_success_response_uses_standard_envelope() -> None:
    response = APIResponse.success(
        data={"id": "example"},
        meta={"request_id": "request-123"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "data": {"id": "example"},
        "meta": {"request_id": "request-123"},
    }


def test_created_response_uses_created_status() -> None:
    response = APIResponse.created(data={"id": "created"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {"data": {"id": "created"}}


def test_updated_response_uses_success_envelope() -> None:
    response = APIResponse.updated(data={"id": "updated"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"data": {"id": "updated"}}


def test_deleted_response_has_no_body() -> None:
    response = APIResponse.deleted()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None


def test_empty_response_has_no_body() -> None:
    response = APIResponse.empty(status_code=status.HTTP_202_ACCEPTED)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data is None


def test_paginated_response_uses_standard_collection_envelope() -> None:
    response = APIResponse.paginated(
        data=[{"id": "one"}],
        pagination={
            "page": 1,
            "page_size": 20,
            "total_count": 1,
            "total_pages": 1,
            "next": None,
            "previous": None,
        },
        meta={"request_id": "request-123"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "data": [{"id": "one"}],
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total_count": 1,
            "total_pages": 1,
            "next": None,
            "previous": None,
        },
        "meta": {"request_id": "request-123"},
    }


def test_error_response_uses_standard_error_envelope() -> None:
    response = APIResponse.error(
        code="validation_error",
        message="Validation failed.",
        status_code=status.HTTP_400_BAD_REQUEST,
        details={"name": ["required"]},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "error": {
            "code": "validation_error",
            "message": "Validation failed.",
            "details": {"name": ["required"]},
        },
    }
