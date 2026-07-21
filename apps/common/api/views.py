"""Reusable API view foundations."""

from __future__ import annotations

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.common.api.mixins import APIResponseMixin


class BaseAPIView(APIResponseMixin, APIView):
    """Base class for non-resource-oriented API views."""


class BaseViewSet(APIResponseMixin, GenericViewSet):
    """Base class for resource-oriented API viewsets."""
