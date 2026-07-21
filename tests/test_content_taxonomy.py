from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.content.models import Category, Tag

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        email="staff@example.com",
        username="staff",
        password="StrongPass123!",
        is_staff=True,
    )


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email="reader@example.com",
        username="reader",
        password="StrongPass123!",
    )


def authenticate(client: APIClient, user) -> None:
    client.force_authenticate(user=user)


@pytest.mark.django_db
def test_category_slug_is_generated_from_name() -> None:
    category = Category.objects.create(name="Software Architecture")

    assert category.slug == "software-architecture"


@pytest.mark.django_db
def test_tag_slug_is_generated_from_name() -> None:
    tag = Tag.objects.create(name="Django REST Framework")

    assert tag.slug == "django-rest-framework"


@pytest.mark.django_db
def test_anyone_can_list_categories(api_client: APIClient) -> None:
    Category.objects.create(name="Architecture", description="System design")

    response = api_client.get(reverse("content:category-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"][0]["name"] == "Architecture"
    assert response.data["pagination"]["total_count"] == 1


@pytest.mark.django_db
def test_anyone_can_retrieve_tags(api_client: APIClient) -> None:
    tag = Tag.objects.create(name="Django")

    response = api_client.get(reverse("content:tag-detail", args=[tag.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["name"] == "Django"


@pytest.mark.django_db
def test_anonymous_users_cannot_create_categories(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("content:category-list"),
        {"name": "Architecture"},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_regular_users_cannot_create_tags(
    api_client: APIClient,
    regular_user,
) -> None:
    authenticate(api_client, regular_user)

    response = api_client.post(
        reverse("content:tag-list"),
        {"name": "Django"},
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["error"]["code"] == "permission_denied"


@pytest.mark.django_db
def test_staff_can_create_update_and_delete_categories(
    api_client: APIClient,
    staff_user,
) -> None:
    authenticate(api_client, staff_user)

    create_response = api_client.post(
        reverse("content:category-list"),
        {
            "name": "Architecture",
            "description": "System design",
            "is_active": True,
        },
        format="json",
    )

    assert create_response.status_code == status.HTTP_201_CREATED
    category_id = create_response.data["data"]["id"]
    assert create_response.data["data"]["slug"] == "architecture"

    update_response = api_client.put(
        reverse("content:category-detail", args=[category_id]),
        {
            "name": "Architecture",
            "description": "Production design",
            "is_active": False,
        },
        format="json",
    )

    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.data["data"]["description"] == "Production design"
    assert update_response.data["data"]["is_active"] is False

    delete_response = api_client.delete(
        reverse("content:category-detail", args=[category_id]),
    )

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.count() == 0
    assert Category.deleted_objects.count() == 1


@pytest.mark.django_db
def test_staff_can_create_update_and_delete_tags(
    api_client: APIClient,
    staff_user,
) -> None:
    authenticate(api_client, staff_user)

    create_response = api_client.post(
        reverse("content:tag-list"),
        {"name": "Django"},
        format="json",
    )

    assert create_response.status_code == status.HTTP_201_CREATED
    tag_id = create_response.data["data"]["id"]
    assert create_response.data["data"]["slug"] == "django"

    update_response = api_client.patch(
        reverse("content:tag-detail", args=[tag_id]),
        {"name": "Django REST"},
        format="json",
    )

    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.data["data"]["name"] == "Django REST"
    assert update_response.data["data"]["slug"] == "django"

    delete_response = api_client.delete(reverse("content:tag-detail", args=[tag_id]))

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert Tag.objects.count() == 0
    assert Tag.deleted_objects.count() == 1


@pytest.mark.django_db
def test_category_search_filters_results(api_client: APIClient) -> None:
    Category.objects.create(name="Architecture", description="System design")
    Category.objects.create(name="Travel", description="Places")

    response = api_client.get(reverse("content:category-list"), {"search": "system"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pagination"]["total_count"] == 1
    assert response.data["data"][0]["name"] == "Architecture"


@pytest.mark.django_db
def test_tag_search_filters_results(api_client: APIClient) -> None:
    Tag.objects.create(name="Django")
    Tag.objects.create(name="Python")

    response = api_client.get(reverse("content:tag-list"), {"search": "django"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pagination"]["total_count"] == 1
    assert response.data["data"][0]["name"] == "Django"


@pytest.mark.django_db
def test_ordering_sorts_categories(api_client: APIClient) -> None:
    Category.objects.create(name="Zebra")
    Category.objects.create(name="Alpha")

    response = api_client.get(reverse("content:category-list"), {"ordering": "-name"})

    assert response.status_code == status.HTTP_200_OK
    assert [item["name"] for item in response.data["data"]] == ["Zebra", "Alpha"]


@pytest.mark.django_db
def test_pagination_limits_category_results(api_client: APIClient) -> None:
    for index in range(3):
        Category.objects.create(name=f"Category {index}")

    response = api_client.get(reverse("content:category-list"), {"page_size": 2})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["data"]) == 2
    assert response.data["pagination"]["page_size"] == 2
    assert response.data["pagination"]["total_count"] == 3


@pytest.mark.django_db
def test_duplicate_category_name_is_rejected(
    api_client: APIClient,
    staff_user,
) -> None:
    Category.objects.create(name="Architecture")
    authenticate(api_client, staff_user)

    response = api_client.post(
        reverse("content:category-list"),
        {"name": "architecture"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data["error"]["details"]


@pytest.mark.django_db
def test_openapi_schema_includes_content_routes(api_client: APIClient) -> None:
    response = api_client.get(reverse("schema"))

    assert response.status_code == status.HTTP_200_OK
    assert "/api/v1/categories/" in response.data["paths"]
    assert "/api/v1/categories/{id}/" in response.data["paths"]
    assert "/api/v1/tags/" in response.data["paths"]
    assert "/api/v1/tags/{id}/" in response.data["paths"]
