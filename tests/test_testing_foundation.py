from __future__ import annotations

from rest_framework import status

from apps.common.responses import APIResponse
from tests.common import (
    BaseAPITestCase,
    BaseFactory,
    BaseTestCase,
    build_api_client,
    build_request_headers,
    build_response_meta,
    merge_dicts,
)


class ExampleFactory(BaseFactory):
    @classmethod
    def defaults(cls) -> dict[str, object]:
        sequence = cls.next_sequence()
        return {
            "id": sequence,
            "name": f"example-{sequence}",
        }


class TestingFoundationUnitTests(BaseTestCase):
    def test_base_factory_builds_default_attributes(self) -> None:
        ExampleFactory.reset_sequence()

        assert ExampleFactory.build() == {"id": 1, "name": "example-1"}

    def test_base_factory_applies_overrides(self) -> None:
        ExampleFactory.reset_sequence()

        assert ExampleFactory.build(name="custom") == {"id": 1, "name": "custom"}

    def test_base_factory_builds_batches(self) -> None:
        ExampleFactory.reset_sequence()

        assert ExampleFactory.build_batch(2) == [
            {"id": 1, "name": "example-1"},
            {"id": 2, "name": "example-2"},
        ]

    def test_merge_dicts_combines_values_in_order(self) -> None:
        assert merge_dicts({"a": 1}, {"a": 2, "b": 3}) == {"a": 2, "b": 3}

    def test_build_response_meta_omits_empty_values(self) -> None:
        assert build_response_meta(request_id="request-123") == {
            "request_id": "request-123"
        }

    def test_response_assertions_validate_success_envelope(self) -> None:
        response = APIResponse.success(data={"ok": True})

        self.assert_success_response(response, data={"ok": True})

    def test_response_assertions_validate_error_envelope(self) -> None:
        response = APIResponse.error(
            code="validation_error",
            message="Validation failed.",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"field": ["required"]},
        )

        self.assert_validation_error(response, details={"field": ["required"]})


class TestingFoundationAPITests(BaseAPITestCase):
    def test_build_headers_returns_request_metadata_headers(self) -> None:
        assert self.build_headers(
            request_id="request-123",
            correlation_id="correlation-123",
        ) == {
            "HTTP_X_REQUEST_ID": "request-123",
            "HTTP_X_CORRELATION_ID": "correlation-123",
        }

    def test_build_api_client_applies_default_headers(self) -> None:
        client = build_api_client(
            headers=build_request_headers(request_id="request-123")
        )

        assert client.defaults["HTTP_X_REQUEST_ID"] == "request-123"

    def test_empty_response_assertion_accepts_no_content(self) -> None:
        response = APIResponse.deleted()

        self.assert_empty_response(response)
