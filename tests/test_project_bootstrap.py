from __future__ import annotations

from django.conf import settings
from django.core.management import call_command


def test_django_settings_load() -> None:
    assert settings.ROOT_URLCONF == "config.urls"
    assert settings.DEFAULT_AUTO_FIELD == "django.db.models.BigAutoField"
    assert "rest_framework" in settings.INSTALLED_APPS
    assert "apps.common" in settings.INSTALLED_APPS
    assert "apps.core" in settings.INSTALLED_APPS


def test_django_system_check_passes() -> None:
    call_command("check")
