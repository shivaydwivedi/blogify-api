from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.bookmarks.models import Bookmark
from apps.comments.models import Comment
from apps.likes.models import Like
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
def reader(db):
    return User.objects.create_user(
        email="reader@example.com",
        username="reader",
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
def published_post(author):
    return Post.objects.create(
        author=author,
        title="Published Post",
        content="Published content",
        status=PostStatus.PUBLISHED,
    )


@pytest.fixture
def draft_post(author):
    return Post.objects.create(
        author=author,
        title="Draft Post",
        content="Draft content",
        status=PostStatus.DRAFT,
    )


def authenticate(client: APIClient, user) -> None:
    client.force_authenticate(user=user)


@pytest.mark.django_db
def test_public_can_list_comments_for_published_post(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    Comment.objects.create(
        post=published_post,
        author=reader,
        content="Useful post.",
    )

    response = api_client.get(
        reverse("comments:post-comments", args=[published_post.id]),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pagination"]["total_count"] == 1
    assert response.data["data"][0]["content"] == "Useful post."


@pytest.mark.django_db
def test_authenticated_user_can_create_comment(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    response = api_client.post(
        reverse("comments:post-comments", args=[published_post.id]),
        {"content": "Great read."},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["data"]["content"] == "Great read."
    assert response.data["data"]["author"]["email"] == reader.email
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_user_cannot_create_comment(
    api_client: APIClient,
    published_post,
) -> None:
    response = api_client.post(
        reverse("comments:post-comments", args=[published_post.id]),
        {"content": "Great read."},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_comments_are_not_allowed_on_draft_posts(
    api_client: APIClient,
    draft_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    response = api_client.post(
        reverse("comments:post-comments", args=[draft_post.id]),
        {"content": "Can I comment?"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"


@pytest.mark.django_db
def test_author_can_update_own_comment(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    comment = Comment.objects.create(
        post=published_post,
        author=reader,
        content="Original",
    )
    authenticate(api_client, reader)

    response = api_client.patch(
        reverse("comments:comment-detail", args=[comment.id]),
        {"content": "Updated"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["content"] == "Updated"
    assert response.data["data"]["is_edited"] is True


@pytest.mark.django_db
def test_non_author_cannot_update_comment(
    api_client: APIClient,
    published_post,
    reader,
    other_user,
) -> None:
    comment = Comment.objects.create(
        post=published_post,
        author=reader,
        content="Original",
    )
    authenticate(api_client, other_user)

    response = api_client.patch(
        reverse("comments:comment-detail", args=[comment.id]),
        {"content": "Updated"},
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["error"]["code"] == "permission_denied"


@pytest.mark.django_db
def test_author_can_delete_own_comment(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    comment = Comment.objects.create(
        post=published_post,
        author=reader,
        content="Original",
    )
    authenticate(api_client, reader)

    response = api_client.delete(reverse("comments:comment-detail", args=[comment.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 0
    assert Comment.deleted_objects.count() == 1


@pytest.mark.django_db
def test_staff_can_delete_any_comment(
    api_client: APIClient,
    published_post,
    reader,
    staff_user,
) -> None:
    comment = Comment.objects.create(
        post=published_post,
        author=reader,
        content="Needs moderation",
    )
    authenticate(api_client, staff_user)

    response = api_client.delete(reverse("comments:comment-detail", args=[comment.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.deleted_objects.count() == 1


@pytest.mark.django_db
def test_comments_support_one_level_replies(
    api_client: APIClient,
    published_post,
    reader,
    other_user,
) -> None:
    parent = Comment.objects.create(
        post=published_post,
        author=reader,
        content="Parent",
    )
    authenticate(api_client, other_user)

    create_response = api_client.post(
        reverse("comments:post-comments", args=[published_post.id]),
        {"content": "Reply", "parent": str(parent.id)},
        format="json",
    )
    list_response = api_client.get(
        reverse("comments:post-comments", args=[published_post.id]),
    )

    assert create_response.status_code == status.HTTP_201_CREATED
    assert str(create_response.data["data"]["parent"]) == str(parent.id)
    assert list_response.data["pagination"]["total_count"] == 1
    assert list_response.data["data"][0]["replies"][0]["content"] == "Reply"


@pytest.mark.django_db
def test_second_level_replies_are_rejected(
    api_client: APIClient,
    published_post,
    reader,
    other_user,
) -> None:
    parent = Comment.objects.create(
        post=published_post,
        author=reader,
        content="Parent",
    )
    reply = Comment.objects.create(
        post=published_post,
        author=other_user,
        parent=parent,
        content="Reply",
    )
    authenticate(api_client, reader)

    response = api_client.post(
        reverse("comments:post-comments", args=[published_post.id]),
        {"content": "Nested", "parent": str(reply.id)},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "parent" in response.data["error"]["details"]


@pytest.mark.django_db
def test_authenticated_user_can_like_and_unlike_post(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    like_response = api_client.post(
        reverse("likes:post-like", args=[published_post.id]),
    )
    duplicate_response = api_client.post(
        reverse("likes:post-like", args=[published_post.id]),
    )
    unlike_response = api_client.delete(
        reverse("likes:post-like", args=[published_post.id]),
    )

    assert like_response.status_code == status.HTTP_201_CREATED
    assert like_response.data["data"]["liked"] is True
    assert like_response.data["data"]["like_count"] == 1
    assert duplicate_response.status_code == status.HTTP_200_OK
    assert duplicate_response.data["data"]["created"] is False
    assert Like.objects.count() == 0
    assert unlike_response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_likes_require_authentication(api_client: APIClient, published_post) -> None:
    response = api_client.post(reverse("likes:post-like", args=[published_post.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_likes_are_only_allowed_on_published_posts(
    api_client: APIClient,
    draft_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    response = api_client.post(reverse("likes:post-like", args=[draft_post.id]))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"


@pytest.mark.django_db
def test_post_detail_exposes_like_and_bookmark_state(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    Like.objects.create(user=reader, post=published_post)
    Bookmark.objects.create(user=reader, post=published_post)
    authenticate(api_client, reader)

    response = api_client.get(reverse("posts:post-detail", args=[published_post.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["like_count"] == 1
    assert response.data["data"]["is_liked"] is True
    assert response.data["data"]["is_bookmarked"] is True


@pytest.mark.django_db
def test_authenticated_user_can_bookmark_and_remove_bookmark(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    bookmark_response = api_client.post(
        reverse("bookmarks:post-bookmark", args=[published_post.id]),
    )
    duplicate_response = api_client.post(
        reverse("bookmarks:post-bookmark", args=[published_post.id]),
    )
    remove_response = api_client.delete(
        reverse("bookmarks:post-bookmark", args=[published_post.id]),
    )

    assert bookmark_response.status_code == status.HTTP_201_CREATED
    assert bookmark_response.data["data"]["bookmarked"] is True
    assert duplicate_response.status_code == status.HTTP_200_OK
    assert duplicate_response.data["data"]["created"] is False
    assert Bookmark.objects.count() == 0
    assert remove_response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_bookmarks_require_authentication(
    api_client: APIClient, published_post
) -> None:
    response = api_client.post(
        reverse("bookmarks:post-bookmark", args=[published_post.id]),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_bookmarks_are_only_allowed_on_published_posts(
    api_client: APIClient,
    draft_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    response = api_client.post(reverse("bookmarks:post-bookmark", args=[draft_post.id]))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"


@pytest.mark.django_db
def test_authenticated_user_can_list_own_bookmarks(
    api_client: APIClient,
    published_post,
    reader,
    other_user,
) -> None:
    Bookmark.objects.create(user=reader, post=published_post)
    other_post = Post.objects.create(
        author=other_user,
        title="Other Post",
        content="Content",
        status=PostStatus.PUBLISHED,
    )
    Bookmark.objects.create(user=other_user, post=other_post)
    authenticate(api_client, reader)

    response = api_client.get(reverse("bookmarks:bookmark-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pagination"]["total_count"] == 1
    assert response.data["data"][0]["post"]["id"] == str(published_post.id)


@pytest.mark.django_db
def test_bookmark_list_requires_authentication(api_client: APIClient) -> None:
    response = api_client.get(reverse("bookmarks:bookmark-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_like_and_bookmark_unique_constraints(published_post, reader) -> None:
    Like.objects.create(user=reader, post=published_post)
    Bookmark.objects.create(user=reader, post=published_post)

    with pytest.raises(IntegrityError), transaction.atomic():
        Like.objects.create(user=reader, post=published_post)

    with pytest.raises(IntegrityError), transaction.atomic():
        Bookmark.objects.create(user=reader, post=published_post)


@pytest.mark.django_db
def test_openapi_schema_includes_engagement_routes(api_client: APIClient) -> None:
    response = api_client.get(reverse("schema"))

    assert response.status_code == status.HTTP_200_OK
    assert "/api/v1/posts/{post_id}/comments/" in response.data["paths"]
    assert "/api/v1/comments/{id}/" in response.data["paths"]
    assert "/api/v1/posts/{post_id}/like/" in response.data["paths"]
    assert "/api/v1/posts/{post_id}/bookmark/" in response.data["paths"]
    assert "/api/v1/bookmarks/" in response.data["paths"]
