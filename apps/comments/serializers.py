"""Serializers for comment APIs."""

from __future__ import annotations

from rest_framework import serializers

from apps.comments.models import Comment
from apps.posts.models import PostStatus
from apps.posts.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serialize comments with one-level replies."""

    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "parent",
            "content",
            "is_edited",
            "created_at",
            "updated_at",
            "replies",
        )
        read_only_fields = (
            "id",
            "post",
            "author",
            "is_edited",
            "created_at",
            "updated_at",
            "replies",
        )

    def get_replies(self, obj: Comment) -> list[dict]:
        if obj.parent_id is not None:
            return []

        replies = obj.replies.filter(is_deleted=False).select_related("author")
        return CommentReplySerializer(
            replies,
            many=True,
            context=self.context,
        ).data

    def validate_parent(self, value: Comment | None) -> Comment | None:
        post = self.context["post"]

        if value is None:
            return value

        if value.post_id != post.id:
            raise serializers.ValidationError(
                "Parent comment must belong to this post."
            )

        if value.parent_id is not None:
            raise serializers.ValidationError("Only one level of replies is supported.")

        return value

    def validate(self, attrs: dict) -> dict:
        post = self.context["post"]
        if post.status != PostStatus.PUBLISHED:
            raise serializers.ValidationError(
                "Comments are only allowed on published posts."
            )
        return attrs

    def create(self, validated_data: dict) -> Comment:
        comment = Comment.objects.create(
            post=self.context["post"],
            author=self.context["request"].user,
            **validated_data,
        )

        from apps.notifications.services import create_comment_notification

        create_comment_notification(comment)
        return comment


class CommentReplySerializer(serializers.ModelSerializer):
    """Serialize one-level comment replies."""

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "parent",
            "content",
            "is_edited",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CommentUpdateSerializer(serializers.ModelSerializer):
    """Validate comment update requests."""

    class Meta:
        model = Comment
        fields = ("content",)

    def update(self, instance: Comment, validated_data: dict) -> Comment:
        instance.content = validated_data["content"]
        instance.is_edited = True
        instance.save(update_fields=("content", "is_edited", "updated_at"))
        return instance
