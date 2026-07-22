from __future__ import annotations

from io import StringIO

from django.conf import settings
from django.core.management import call_command
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


def test_bootstrap_superuser_skips_when_environment_is_missing(
    django_user_model,
    monkeypatch,
) -> None:
    monkeypatch.delenv("DJANGO_SUPERUSER_USERNAME", raising=False)
    monkeypatch.delenv("DJANGO_SUPERUSER_EMAIL", raising=False)
    monkeypatch.delenv("DJANGO_SUPERUSER_PASSWORD", raising=False)
    output = StringIO()

    call_command("bootstrap_superuser", stdout=output)

    assert output.getvalue().strip() == (
        "Skipping superuser creation. Missing environment variables: "
        "DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, "
        "DJANGO_SUPERUSER_PASSWORD"
    )
    assert django_user_model.objects.filter(is_superuser=True).count() == 0


def test_bootstrap_superuser_creates_initial_admin(
    django_user_model,
    monkeypatch,
) -> None:
    monkeypatch.setenv("DJANGO_SUPERUSER_USERNAME", "admin")
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "Str0ngAdminPass!")
    output = StringIO()

    call_command("bootstrap_superuser", stdout=output)

    user = django_user_model.objects.get(email="admin@example.com")
    assert output.getvalue().strip() == "Superuser created successfully."
    assert user.username == "admin"
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.check_password("Str0ngAdminPass!")


def test_bootstrap_superuser_is_idempotent(
    django_user_model,
    monkeypatch,
) -> None:
    django_user_model.objects.create_superuser(
        email="existing@example.com",
        username="existing",
        password="Str0ngAdminPass!",
    )
    monkeypatch.setenv("DJANGO_SUPERUSER_USERNAME", "admin")
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "Str0ngAdminPass!")
    output = StringIO()

    call_command("bootstrap_superuser", stdout=output)

    assert output.getvalue().strip() == "Superuser already exists."
    assert django_user_model.objects.filter(is_superuser=True).count() == 1
