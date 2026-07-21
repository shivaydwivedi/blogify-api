"""Notification creation helpers."""

from __future__ import annotations

from apps.notifications.models import Notification, NotificationType


def create_email_verified_notification(user) -> Notification:
    """Notify a user that their email was verified."""

    return Notification.objects.create(
        recipient=user,
        actor=None,
        type=NotificationType.EMAIL_VERIFIED,
        title="Email verified",
        message="Your Blogify email address has been verified.",
    )


def create_post_liked_notification(like) -> Notification | None:
    """Notify a post author when another user likes their post."""

    post = like.post
    if post.author_id == like.user_id:
        return None

    return Notification.objects.create(
        recipient=post.author,
        actor=like.user,
        type=NotificationType.POST_LIKED,
        title="New like on your post",
        message=f"{like.user.username} liked your post.",
        related_post=post,
    )


def create_comment_notification(comment) -> Notification | None:
    """Notify the relevant owner when a post is commented on or replied to."""

    if comment.parent_id is not None:
        if comment.parent.author_id == comment.author_id:
            return None

        return Notification.objects.create(
            recipient=comment.parent.author,
            actor=comment.author,
            type=NotificationType.COMMENT_REPLIED,
            title="New reply to your comment",
            message=f"{comment.author.username} replied to your comment.",
            related_post=comment.post,
            related_comment=comment,
        )

    if comment.post.author_id == comment.author_id:
        return None

    return Notification.objects.create(
        recipient=comment.post.author,
        actor=comment.author,
        type=NotificationType.POST_COMMENTED,
        title="New comment on your post",
        message=f"{comment.author.username} commented on your post.",
        related_post=comment.post,
        related_comment=comment,
    )
