from __future__ import annotations

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.core.views import HealthCheckAPIView


def test_whitenoise_static_storage_is_configured() -> None:
    assert (
        settings.STORAGES["staticfiles"]["BACKEND"]
        == "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )


def test_health_endpoint_reports_healthy_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(HealthCheckAPIView, "check_database", lambda self: "ok")
    monkeypatch.setattr(HealthCheckAPIView, "check_redis", lambda self: "ok")

    response = APIClient().get(reverse("core:health"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "status": "healthy",
        "database": "ok",
        "redis": "ok",
        "version": "1.0.0",
    }


def test_health_endpoint_reports_unhealthy_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(HealthCheckAPIView, "check_database", lambda self: "ok")
    monkeypatch.setattr(HealthCheckAPIView, "check_redis", lambda self: "error")

    response = APIClient().get(reverse("core:health"))

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.data == {
        "status": "unhealthy",
        "database": "ok",
        "redis": "error",
        "version": "1.0.0",
    }
