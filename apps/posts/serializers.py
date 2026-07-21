"""Serializers for post APIs."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.content.models import Category, Tag
from apps.content.serializers import CategorySerializer, TagSerializer
from apps.posts.models import Post, PostStatus

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Expose safe author information."""

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name")
        read_only_fields = fields


class PostListSerializer(serializers.ModelSerializer):
    """Serialize post collection items."""

    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "category",
            "tags",
            "title",
            "slug",
            "excerpt",
            "status",
            "is_featured",
            "published_at",
            "reading_time",
            "view_count",
            "like_count",
            "is_liked",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields

    def get_like_count(self, obj: Post) -> int:
        return obj.likes.count()

    def get_is_liked(self, obj: Post) -> bool:
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", False):
            return False

        return obj.likes.filter(user=user).exists()


class PostDetailSerializer(PostListSerializer):
    """Serialize full post details."""

    is_bookmarked = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + (
            "content",
            "featured_image",
            "is_bookmarked",
        )

    def get_is_bookmarked(self, obj: Post) -> bool:
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", False):
            return False

        return obj.bookmarks.filter(user=user).exists()


class PostWriteSerializer(serializers.ModelSerializer):
    """Validate post create and update requests."""

    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        source="tags",
        queryset=Tag.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "excerpt",
            "content",
            "featured_image",
            "category_id",
            "tag_ids",
            "status",
            "is_featured",
        )

    def validate_status(self, value: str) -> str:
        if value not in PostStatus.values:
            raise serializers.ValidationError("Invalid post status.")
        return value

    def create(self, validated_data: dict) -> Post:
        tags = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance: Post, validated_data: dict) -> Post:
        tags = validated_data.pop("tags", None)

        for field_name, value in validated_data.items():
            setattr(instance, field_name, value)

        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance
