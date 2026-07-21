from __future__ import annotations

import pytest
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from apps.common.api import (
    APIResponseMixin,
    BaseAPIView,
    BaseFilter,
    BasePagination,
    BasePermission,
    BaseSerializer,
    BaseViewSet,
)


class ResponseHarness(APIResponseMixin):
    def __init__(self, request=None):
        self.request = request


class ExampleSerializer(BaseSerializer):
    server_controlled_fields = ("owner_id",)

    name = serializers.CharField()
    owner_id = serializers.CharField(required=False)


def test_common_api_components_import() -> None:
    assert issubclass(BaseAPIView, APIResponseMixin)
    assert issubclass(BaseViewSet, APIResponseMixin)
    assert issubclass(BaseSerializer, serializers.Serializer)
    assert issubclass(BasePermission, object)
    assert issubclass(BasePagination, object)
    assert issubclass(BaseFilter, object)


def test_success_response_uses_standard_envelope() -> None:
    request = APIRequestFactory().get("/", HTTP_X_REQUEST_ID="request-123")
    harness = ResponseHarness(request=request)

    response = harness.success_response({"id": "example"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "data": {"id": "example"},
        "meta": {"request_id": "request-123"},
    }


def test_error_response_uses_standard_envelope() -> None:
    request = APIRequestFactory().get("/", HTTP_X_CORRELATION_ID="correlation-123")
    harness = ResponseHarness(request=request)

    response = harness.error_response(
        code="invalid_request",
        message="Invalid request.",
        status_code=status.HTTP_400_BAD_REQUEST,
        details=[{"field": "name"}],
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "error": {
            "code": "invalid_request",
            "message": "Invalid request.",
            "details": [{"field": "name"}],
        },
        "meta": {"correlation_id": "correlation-123"},
    }


def test_base_serializer_removes_server_controlled_fields() -> None:
    serializer = ExampleSerializer(data={"name": "Example", "owner_id": "user-1"})

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == {"name": "Example"}


def test_base_permission_exposes_error_code() -> None:
    permission = BasePermission()

    assert permission.get_error_code() == "permission_denied"


@pytest.mark.parametrize(
    "requested_page_size, expected_page_size", [(None, 20), (5, 5)]
)
def test_base_pagination_returns_standard_metadata(
    requested_page_size,
    expected_page_size,
) -> None:
    factory = APIRequestFactory()
    query = {} if requested_page_size is None else {"page_size": requested_page_size}
    request = Request(factory.get("/", query))
    paginator = BasePagination()

    page = paginator.paginate_queryset(list(range(30)), request)
    response = paginator.get_paginated_response(page)

    assert response.data["data"] == page
    assert response.data["pagination"]["page"] == 1
    assert response.data["pagination"]["page_size"] == expected_page_size
    assert response.data["pagination"]["total_count"] == 30
    assert response.data["pagination"]["total_pages"] >= 2
