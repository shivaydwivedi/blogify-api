from __future__ import annotations

import uuid

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.accounts.admin import UserAdmin
from apps.accounts.models import User


@pytest.mark.django_db
def test_custom_user_model_is_configured() -> None:
    user_model = get_user_model()

    assert user_model is User
    assert user_model.USERNAME_FIELD == "email"
    assert user_model.REQUIRED_FIELDS == ["username"]


@pytest.mark.django_db
def test_user_uses_uuid_primary_key() -> None:
    user = User.objects.create_user(
        email="author@example.com",
        username="author",
        password="secure-password",
    )

    assert isinstance(user.id, uuid.UUID)


@pytest.mark.django_db
def test_create_user_normalizes_email_and_sets_defaults() -> None:
    user = User.objects.create_user(
        email="Author@Example.COM",
        username="author",
        password="secure-password",
    )

    assert user.email == "Author@example.com"
    assert user.check_password("secure-password")
    assert user.email_verified is False
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.date_joined is not None
    assert str(user) == "Author@example.com"


@pytest.mark.django_db
def test_create_user_requires_email_and_username() -> None:
    with pytest.raises(ValueError, match="email address"):
        User.objects.create_user(email="", username="author", password="password")

    with pytest.raises(ValueError, match="username"):
        User.objects.create_user(
            email="author@example.com",
            username="",
            password="password",
        )


@pytest.mark.django_db
def test_create_user_validates_email_and_username() -> None:
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="not-an-email",
            username="valid_username",
            password="password",
        )

    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="valid@example.com",
            username="invalid username",
            password="password",
        )


@pytest.mark.django_db
def test_create_superuser_requires_admin_flags() -> None:
    superuser = User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        password="secure-password",
    )

    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.is_active is True

    with pytest.raises(ValueError, match="is_staff=True"):
        User.objects.create_superuser(
            email="bad-staff@example.com",
            username="badstaff",
            password="password",
            is_staff=False,
        )

    with pytest.raises(ValueError, match="is_superuser=True"):
        User.objects.create_superuser(
            email="bad-admin@example.com",
            username="badadmin",
            password="password",
            is_superuser=False,
        )


def test_user_admin_is_registered() -> None:
    assert admin.site.is_registered(User)
    assert isinstance(admin.site._registry[User], UserAdmin)
