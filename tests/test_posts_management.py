from __future__ import annotations

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.content.models import Category, Tag
from apps.posts.models import Post, PostStatus

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def author(db):
    return User.objects.create_user(
        email="author@example.com",
        username="author",
        password="StrongPass123!",
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        email="other@example.com",
        username="other",
        password="StrongPass123!",
    )


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        email="staff@example.com",
        username="staff",
        password="StrongPass123!",
        is_staff=True,
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="Engineering")


@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Django")


def authenticate(client: APIClient, user) -> None:
    client.force_authenticate(user=user)


def post_payload(category=None, tags=None, **overrides) -> dict:
    payload = {
        "title": "Building Reliable APIs",
        "excerpt": "Practical notes on API design.",
        "content": "Reliable APIs need clear contracts and useful tests. " * 45,
        "status": PostStatus.DRAFT,
        "is_featured": False,
    }
    if category is not None:
        payload["category_id"] = str(category.id)
    if tags is not None:
        payload["tag_ids"] = [str(item.id) for item in tags]
    payload.update(overrides)
    return payload


@pytest.mark.django_db
def test_post_slug_reading_time_and_publish_fields_are_generated(
    author,
    category,
    tag,
) -> None:
    post = Post.objects.create(
        author=author,
        category=category,
        title="Building Reliable APIs",
        excerpt="Practical notes.",
        content="word " * 260,
        status=PostStatus.PUBLISHED,
    )
    post.tags.set([tag])

    assert post.slug == "building-reliable-apis"
    assert post.reading_time == 2
    assert post.published_at is not None


@pytest.mark.django_db
def test_duplicate_post_titles_get_unique_slugs(author) -> None:
    first = Post.objects.create(
        author=author,
        title="Same Title",
        content="First post",
    )
    second = Post.objects.create(
        author=author,
        title="Same Title",
        content="Second post",
    )

    assert first.slug == "same-title"
    assert second.slug == "same-title-2"


@pytest.mark.django_db
def test_authenticated_author_can_create_post(
    api_client: APIClient,
    author,
    category,
    tag,
) -> None:
    authenticate(api_client, author)

    response = api_client.post(
        reverse("posts:post-list"),
        post_payload(category=category, tags=[tag]),
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["data"]["author"]["email"] == author.email
    assert response.data["data"]["category"]["name"] == category.name
    assert response.data["data"]["tags"][0]["name"] == tag.name
    assert response.data["data"]["slug"] == "building-reliable-apis"
    assert Post.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_user_cannot_create_post(api_client: APIClient, category) -> None:
    response = api_client.post(
        reverse("posts:post-list"),
        post_payload(category=category),
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_public_can_view_published_posts(api_client: APIClient, author) -> None:
    published = Post.objects.create(
        author=author,
        title="Published Post",
        content="Published content",
        status=PostStatus.PUBLISHED,
    )

    list_response = api_client.get(reverse("posts:post-list"))
    detail_response = api_client.get(reverse("posts:post-detail", args=[published.id]))

    assert list_response.status_code == status.HTTP_200_OK
    assert list_response.data["pagination"]["total_count"] == 1
    assert detail_response.status_code == status.HTTP_200_OK
    assert detail_response.data["data"]["title"] == "Published Post"


@pytest.mark.django_db
def test_public_cannot_view_draft_posts(api_client: APIClient, author) -> None:
    draft = Post.objects.create(
        author=author,
        title="Draft Post",
        content="Draft content",
        status=PostStatus.DRAFT,
    )

    list_response = api_client.get(reverse("posts:post-list"))
    detail_response = api_client.get(reverse("posts:post-detail", args=[draft.id]))

    assert list_response.status_code == status.HTTP_200_OK
    assert list_response.data["pagination"]["total_count"] == 0
    assert detail_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_author_can_view_and_update_own_draft(api_client: APIClient, author) -> None:
    draft = Post.objects.create(
        author=author,
        title="Draft Post",
        content="Draft content",
        status=PostStatus.DRAFT,
    )
    authenticate(api_client, author)

    retrieve_response = api_client.get(reverse("posts:post-detail", args=[draft.id]))
    update_response = api_client.patch(
        reverse("posts:post-detail", args=[draft.id]),
        {"excerpt": "Updated excerpt"},
        format="json",
    )

    assert retrieve_response.status_code == status.HTTP_200_OK
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.data["data"]["excerpt"] == "Updated excerpt"


@pytest.mark.django_db
def test_non_author_cannot_update_published_post(
    api_client: APIClient,
    author,
    other_user,
) -> None:
    post = Post.objects.create(
        author=author,
        title="Published Post",
        content="Published content",
        status=PostStatus.PUBLISHED,
    )
    authenticate(api_client, other_user)

    response = api_client.patch(
        reverse("posts:post-detail", args=[post.id]),
        {"title": "Hijacked"},
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["error"]["code"] == "permission_denied"


@pytest.mark.django_db
def test_staff_can_update_and_delete_any_post(
    api_client: APIClient,
    author,
    staff_user,
) -> None:
    post = Post.objects.create(
        author=author,
        title="Draft Post",
        content="Draft content",
        status=PostStatus.DRAFT,
    )
    authenticate(api_client, staff_user)

    update_response = api_client.patch(
        reverse("posts:post-detail", args=[post.id]),
        {"title": "Reviewed Draft"},
        format="json",
    )
    delete_response = api_client.delete(reverse("posts:post-detail", args=[post.id]))

    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.data["data"]["title"] == "Reviewed Draft"
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert Post.objects.count() == 0
    assert Post.deleted_objects.count() == 1


@pytest.mark.django_db
def test_publish_workflow_sets_published_at(api_client: APIClient, author) -> None:
    post = Post.objects.create(
        author=author,
        title="Draft Post",
        content="Draft content",
        status=PostStatus.DRAFT,
    )
    authenticate(api_client, author)

    response = api_client.patch(
        reverse("posts:post-detail", args=[post.id]),
        {"status": PostStatus.PUBLISHED},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.status == PostStatus.PUBLISHED
    assert post.published_at is not None


@pytest.mark.django_db
def test_posts_can_be_filtered_by_category_tag_author_status_and_featured(
    api_client: APIClient,
    author,
    other_user,
    category,
    tag,
) -> None:
    matching = Post.objects.create(
        author=author,
        category=category,
        title="Matching Post",
        content="Content",
        status=PostStatus.PUBLISHED,
        is_featured=True,
    )
    matching.tags.set([tag])
    Post.objects.create(
        author=other_user,
        title="Other Post",
        content="Content",
        status=PostStatus.PUBLISHED,
    )

    response = api_client.get(
        reverse("posts:post-list"),
        {
            "category": str(category.id),
            "tag": str(tag.id),
            "author": str(author.id),
            "status": PostStatus.PUBLISHED,
            "featured": "true",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pagination"]["total_count"] == 1
    assert response.data["data"][0]["id"] == str(matching.id)


@pytest.mark.django_db
def test_posts_can_be_searched(api_client: APIClient, author) -> None:
    Post.objects.create(
        author=author,
        title="Architecture Notes",
        excerpt="Reliable systems",
        content="Content",
        status=PostStatus.PUBLISHED,
    )
    Post.objects.create(
        author=author,
        title="Travel Notes",
        excerpt="Places",
        content="Content",
        status=PostStatus.PUBLISHED,
    )

    response = api_client.get(reverse("posts:post-list"), {"search": "reliable"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pagination"]["total_count"] == 1
    assert response.data["data"][0]["title"] == "Architecture Notes"


@pytest.mark.django_db
def test_posts_support_ordering_aliases(api_client: APIClient, author) -> None:
    older = Post.objects.create(
        author=author,
        title="Older Post",
        content="Content",
        status=PostStatus.PUBLISHED,
    )
    newer = Post.objects.create(
        author=author,
        title="Newer Post",
        content="Content",
        status=PostStatus.PUBLISHED,
    )
    now = timezone.now()
    Post.objects.filter(pk=older.pk).update(created_at=now)
    Post.objects.filter(pk=newer.pk).update(created_at=now + timedelta(minutes=1))

    newest_response = api_client.get(
        reverse("posts:post-list"),
        {"ordering": "newest"},
    )
    title_response = api_client.get(
        reverse("posts:post-list"),
        {"ordering": "title"},
    )

    assert newest_response.status_code == status.HTTP_200_OK
    assert newest_response.data["data"][0]["title"] == "Newer Post"
    assert [item["title"] for item in title_response.data["data"]] == [
        "Newer Post",
        "Older Post",
    ]


@pytest.mark.django_db
def test_posts_are_paginated(api_client: APIClient, author) -> None:
    for index in range(3):
        Post.objects.create(
            author=author,
            title=f"Post {index}",
            content="Content",
            status=PostStatus.PUBLISHED,
        )

    response = api_client.get(reverse("posts:post-list"), {"page_size": 2})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["data"]) == 2
    assert response.data["pagination"]["page_size"] == 2
    assert response.data["pagination"]["total_count"] == 3


@pytest.mark.django_db
def test_openapi_schema_includes_post_routes(api_client: APIClient) -> None:
    response = api_client.get(reverse("schema"))

    assert response.status_code == status.HTTP_200_OK
    assert "/api/v1/posts/" in response.data["paths"]
    assert "/api/v1/posts/{id}/" in response.data["paths"]
