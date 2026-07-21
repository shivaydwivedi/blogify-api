from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.comments.models import Comment
from apps.notifications.models import Notification, NotificationType
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
def published_post(author):
    return Post.objects.create(
        author=author,
        title="Published Post",
        content="Published content",
        status=PostStatus.PUBLISHED,
    )


def authenticate(client: APIClient, user) -> None:
    client.force_authenticate(user=user)


def extract_verification_token(email_body: str) -> str:
    for word in email_body.split():
        if "/api/v1/auth/verify-email/" in word:
            parsed = urlparse(word)
            return parse_qs(parsed.query)["token"][0]

    raise AssertionError("Verification URL not found in email body.")


@pytest.mark.django_db
def test_registration_queues_verification_email(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("accounts:register"),
        {
            "email": "new-user@example.com",
            "username": "newuser",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
            "first_name": "New",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Verify your Blogify account"
    assert "New" in mail.outbox[0].body
    assert "/api/v1/auth/verify-email/" in mail.outbox[0].body
    assert mail.outbox[0].alternatives[0][1] == "text/html"


@pytest.mark.django_db
def test_verification_token_marks_email_verified(api_client: APIClient) -> None:
    user = User.objects.create_user(
        email="verify@example.com",
        username="verify",
        password="StrongPass123!",
    )
    from apps.accounts.tasks import send_verification_email

    send_verification_email.delay(str(user.id))
    token = extract_verification_token(mail.outbox[-1].body)

    response = api_client.get(reverse("accounts:verify-email"), {"token": token})

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email_verified is True
    assert Notification.objects.filter(
        recipient=user,
        type=NotificationType.EMAIL_VERIFIED,
    ).exists()


@pytest.mark.django_db
def test_verification_token_is_one_time(api_client: APIClient) -> None:
    user = User.objects.create_user(
        email="one-time@example.com",
        username="onetime",
        password="StrongPass123!",
    )
    from apps.accounts.tasks import send_verification_email

    send_verification_email.delay(str(user.id))
    token = extract_verification_token(mail.outbox[-1].body)

    first_response = api_client.get(reverse("accounts:verify-email"), {"token": token})
    second_response = api_client.get(reverse("accounts:verify-email"), {"token": token})

    assert first_response.status_code == status.HTTP_200_OK
    assert second_response.status_code == status.HTTP_400_BAD_REQUEST
    assert second_response.data["error"]["code"] == "validation_error"


@pytest.mark.django_db
def test_invalid_verification_token_is_rejected(api_client: APIClient) -> None:
    response = api_client.get(
        reverse("accounts:verify-email"),
        {"token": "not-a-valid-token"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "validation_error"


@pytest.mark.django_db
@override_settings(EMAIL_VERIFICATION_TOKEN_MAX_AGE_SECONDS=-1)
def test_expired_verification_token_is_rejected(api_client: APIClient) -> None:
    user = User.objects.create_user(
        email="expired@example.com",
        username="expired",
        password="StrongPass123!",
    )
    from apps.accounts.tokens import generate_email_verification_token

    token = generate_email_verification_token(user)

    response = api_client.get(reverse("accounts:verify-email"), {"token": token})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "expired" in response.data["error"]["message"]


@pytest.mark.django_db
def test_authenticated_user_can_resend_verification_email(
    api_client: APIClient,
    reader,
) -> None:
    authenticate(api_client, reader)

    response = api_client.post(reverse("accounts:resend-verification"))

    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [reader.email]


@pytest.mark.django_db
def test_verified_user_resend_does_not_send_email(
    api_client: APIClient, reader
) -> None:
    reader.email_verified = True
    reader.save(update_fields=("email_verified",))
    authenticate(api_client, reader)

    response = api_client.post(reverse("accounts:resend-verification"))

    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_like_creates_notification_for_post_author(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    response = api_client.post(reverse("likes:post-like", args=[published_post.id]))

    assert response.status_code == status.HTTP_201_CREATED
    notification = Notification.objects.get()
    assert notification.recipient == published_post.author
    assert notification.actor == reader
    assert notification.type == NotificationType.POST_LIKED
    assert notification.related_post == published_post


@pytest.mark.django_db
def test_comment_creates_notification_for_post_author(
    api_client: APIClient,
    published_post,
    reader,
) -> None:
    authenticate(api_client, reader)

    response = api_client.post(
        reverse("comments:post-comments", args=[published_post.id]),
        {"content": "Great post."},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    notification = Notification.objects.get()
    assert notification.recipient == published_post.author
    assert notification.actor == reader
    assert notification.type == NotificationType.POST_COMMENTED


@pytest.mark.django_db
def test_reply_creates_notification_for_parent_comment_author(
    api_client: APIClient,
    published_post,
    reader,
    other_user,
) -> None:
    parent = Comment.objects.create(
        post=published_post,
        author=reader,
        content="Parent comment",
    )
    authenticate(api_client, other_user)

    response = api_client.post(
        reverse("comments:post-comments", args=[published_post.id]),
        {"content": "Reply", "parent": str(parent.id)},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    notification = Notification.objects.get()
    assert notification.recipient == reader
    assert notification.actor == other_user
    assert notification.type == NotificationType.COMMENT_REPLIED


@pytest.mark.django_db
def test_user_can_list_own_notifications(api_client: APIClient, author, reader) -> None:
    Notification.objects.create(
        recipient=author,
        actor=reader,
        type=NotificationType.POST_LIKED,
        title="New like",
        message="Reader liked your post.",
    )
    Notification.objects.create(
        recipient=reader,
        actor=author,
        type=NotificationType.EMAIL_VERIFIED,
        title="Email verified",
        message="Verified.",
    )
    authenticate(api_client, author)

    response = api_client.get(reverse("notifications:notification-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pagination"]["total_count"] == 1
    assert response.data["data"][0]["recipient"] == author.id


@pytest.mark.django_db
def test_notification_list_requires_authentication(api_client: APIClient) -> None:
    response = api_client.get(reverse("notifications:notification-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_user_can_mark_own_notification_read(
    api_client: APIClient,
    author,
    reader,
) -> None:
    notification = Notification.objects.create(
        recipient=author,
        actor=reader,
        type=NotificationType.POST_LIKED,
        title="New like",
        message="Reader liked your post.",
    )
    authenticate(api_client, author)

    response = api_client.patch(
        reverse("notifications:notification-read", args=[notification.id]),
    )

    assert response.status_code == status.HTTP_200_OK
    notification.refresh_from_db()
    assert notification.is_read is True


@pytest.mark.django_db
def test_user_cannot_mark_another_users_notification_read(
    api_client: APIClient,
    author,
    reader,
) -> None:
    notification = Notification.objects.create(
        recipient=author,
        actor=reader,
        type=NotificationType.POST_LIKED,
        title="New like",
        message="Reader liked your post.",
    )
    authenticate(api_client, reader)

    response = api_client.patch(
        reverse("notifications:notification-read", args=[notification.id]),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_mark_all_notifications_read(
    api_client: APIClient,
    author,
    reader,
) -> None:
    Notification.objects.create(
        recipient=author,
        actor=reader,
        type=NotificationType.POST_LIKED,
        title="New like",
        message="Reader liked your post.",
    )
    Notification.objects.create(
        recipient=author,
        actor=reader,
        type=NotificationType.POST_COMMENTED,
        title="New comment",
        message="Reader commented on your post.",
    )
    authenticate(api_client, author)

    response = api_client.patch(reverse("notifications:notification-read-all"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["updated_count"] == 2
    assert Notification.objects.filter(recipient=author, is_read=False).count() == 0


@pytest.mark.django_db
def test_openapi_schema_includes_communication_routes(api_client: APIClient) -> None:
    response = api_client.get(reverse("schema"))

    assert response.status_code == status.HTTP_200_OK
    assert "/api/v1/auth/resend-verification/" in response.data["paths"]
    assert "/api/v1/auth/verify-email/" in response.data["paths"]
    assert "/api/v1/notifications/" in response.data["paths"]
    assert "/api/v1/notifications/{id}/read/" in response.data["paths"]
    assert "/api/v1/notifications/read-all/" in response.data["paths"]
