"""Reusable base test cases."""

from __future__ import annotations

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase

from tests.common.assertions import ResponseAssertions
from tests.common.clients import build_request_headers


class BaseTestCase(ResponseAssertions, TestCase):
    """Base class for non-API tests."""

    maxDiff = None


class BaseAPITestCase(ResponseAssertions, APITestCase):
    """Base class for API tests."""

    client: APIClient
    maxDiff = None

    def build_headers(
        self,
        *,
        request_id: str | None = None,
        correlation_id: str | None = None,
    ) -> dict[str, str]:
        return build_request_headers(
            request_id=request_id,
            correlation_id=correlation_id,
        )
