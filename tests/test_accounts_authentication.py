from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="reader@example.com",
        username="reader",
        password="StrongPass123!",
        first_name="Reader",
        last_name="Example",
    )


def auth_header(access_token: str) -> dict[str, str]:
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


def register_payload(**overrides):
    payload = {
        "email": "author@example.com",
        "username": "author",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
        "first_name": "Author",
        "last_name": "Example",
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
def test_registration_creates_user(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("accounts:register"),
        register_payload(email="Author@Example.COM"),
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["data"]["email"] == "Author@example.com"
    assert response.data["data"]["username"] == "author"
    assert response.data["data"]["email_verified"] is False
    assert "password" not in response.data["data"]
    assert User.objects.filter(email="Author@example.com").exists()


@pytest.mark.django_db
def test_registration_rejects_duplicate_email(
    api_client: APIClient,
    user,
) -> None:
    response = api_client.post(
        reverse("accounts:register"),
        register_payload(email=user.email),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"
    assert "email" in response.data["error"]["details"]


@pytest.mark.django_db
def test_registration_requires_password_confirmation(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("accounts:register"),
        register_payload(password_confirm="DifferentPass123!"),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"
    assert "password_confirm" in response.data["error"]["details"]


@pytest.mark.django_db
def test_registration_enforces_strong_password(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("accounts:register"),
        register_payload(password="short", password_confirm="short"),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"
    assert "password" in response.data["error"]["details"]


@pytest.mark.django_db
def test_login_returns_jwt_token_pair(api_client: APIClient, user) -> None:
    response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "StrongPass123!"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["tokens"]["access"]
    assert response.data["data"]["tokens"]["refresh"]
    assert response.data["data"]["user"]["email"] == user.email


@pytest.mark.django_db
def test_login_rejects_invalid_credentials(api_client: APIClient, user) -> None:
    response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "wrong-password"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"


@pytest.mark.django_db
def test_refresh_rotates_jwt_refresh_token(api_client: APIClient, user) -> None:
    login_response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "StrongPass123!"},
        format="json",
    )
    refresh_token = login_response.data["data"]["tokens"]["refresh"]

    response = api_client.post(
        reverse("accounts:refresh"),
        {"refresh": refresh_token},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["tokens"]["access"]
    assert response.data["data"]["tokens"]["refresh"]
    assert response.data["data"]["tokens"]["refresh"] != refresh_token


@pytest.mark.django_db
def test_logout_blacklists_refresh_token(api_client: APIClient, user) -> None:
    login_response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "StrongPass123!"},
        format="json",
    )
    access_token = login_response.data["data"]["tokens"]["access"]
    refresh_token = login_response.data["data"]["tokens"]["refresh"]

    response = api_client.post(
        reverse("accounts:logout"),
        {"refresh": refresh_token},
        format="json",
        **auth_header(access_token),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert BlacklistedToken.objects.count() == 1


@pytest.mark.django_db
def test_current_user_requires_authentication(api_client: APIClient) -> None:
    response = api_client.get(reverse("accounts:me"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_current_user_returns_authenticated_user(
    api_client: APIClient,
    user,
) -> None:
    login_response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "StrongPass123!"},
        format="json",
    )
    access_token = login_response.data["data"]["tokens"]["access"]

    response = api_client.get(
        reverse("accounts:me"),
        **auth_header(access_token),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["email"] == user.email


@pytest.mark.django_db
def test_change_password_requires_authentication(api_client: APIClient) -> None:
    response = api_client.put(
        reverse("accounts:change-password"),
        {
            "current_password": "StrongPass123!",
            "new_password": "NewStrongPass123!",
            "new_password_confirm": "NewStrongPass123!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_change_password_updates_password(api_client: APIClient, user) -> None:
    login_response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "StrongPass123!"},
        format="json",
    )
    access_token = login_response.data["data"]["tokens"]["access"]

    response = api_client.put(
        reverse("accounts:change-password"),
        {
            "current_password": "StrongPass123!",
            "new_password": "NewStrongPass123!",
            "new_password_confirm": "NewStrongPass123!",
        },
        format="json",
        **auth_header(access_token),
    )

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password("NewStrongPass123!")

    old_password_response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "StrongPass123!"},
        format="json",
    )
    assert old_password_response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_openapi_schema_includes_authentication_routes(api_client: APIClient) -> None:
    response = api_client.get(reverse("schema"))

    assert response.status_code == status.HTTP_200_OK
    assert "/api/v1/auth/register/" in response.data["paths"]
    assert "/api/v1/auth/login/" in response.data["paths"]
    assert "/api/v1/auth/refresh/" in response.data["paths"]
    assert "/api/v1/auth/logout/" in response.data["paths"]
    assert "/api/v1/auth/me/" in response.data["paths"]
    assert "/api/v1/auth/change-password/" in response.data["paths"]
