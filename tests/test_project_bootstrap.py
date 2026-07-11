from __future__ import annotations

from django.conf import settings
from django.core.management import call_command

from config.settings.env import get_bool, get_int, get_list


def test_django_settings_load() -> None:
    assert settings.ROOT_URLCONF == "config.urls"
    assert settings.DEFAULT_AUTO_FIELD == "django.db.models.BigAutoField"
    assert "rest_framework" in settings.INSTALLED_APPS
    assert "apps.common" in settings.INSTALLED_APPS
    assert "apps.core" in settings.INSTALLED_APPS


def test_django_system_check_passes() -> None:
    call_command("check")


def test_environment_helpers_parse_typed_values(monkeypatch) -> None:
    monkeypatch.setenv("BLOGIFY_TEST_BOOL", "true")
    monkeypatch.setenv("BLOGIFY_TEST_INT", "42")
    monkeypatch.setenv("BLOGIFY_TEST_LIST", "alpha,beta,gamma")

    assert get_bool("BLOGIFY_TEST_BOOL") is True
    assert get_int("BLOGIFY_TEST_INT") == 42
    assert get_list("BLOGIFY_TEST_LIST") == ["alpha", "beta", "gamma"]
