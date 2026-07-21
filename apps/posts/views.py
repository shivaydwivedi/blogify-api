"""ViewSets for post APIs."""

from __future__ import annotations

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, mixins, status

from apps.common.api import BasePagination, BaseViewSet
from apps.common.responses import APIResponse
from apps.posts.filters import PostFilter
from apps.posts.models import Post, PostStatus
from apps.posts.permissions import CanAccessPost
from apps.posts.serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostWriteSerializer,
)


@extend_schema(tags=["Posts"])
class PostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """CRUD API for posts."""

    permission_classes = (CanAccessPost,)
    pagination_class = BasePagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = PostFilter
    search_fields = ("title", "excerpt", "content")
    ordering = ("-created_at",)
    ordering_fields = ("created_at", "title", "published_at")

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("author", "category")
            .prefetch_related("tags")
            .distinct()
        )
        user = self.request.user

        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return queryset

        if getattr(user, "is_authenticated", False):
            return queryset.filter(
                Q(status=PostStatus.PUBLISHED) | Q(author=user),
            )

        return queryset.filter(status=PostStatus.PUBLISHED)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action in {"create", "update", "partial_update"}:
            return PostWriteSerializer
        return PostDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering = request.query_params.get("ordering")

        if ordering == "newest":
            queryset = queryset.order_by("-created_at")
        elif ordering == "oldest":
            queryset = queryset.order_by("created_at")

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PostListSerializer(
                page,
                many=True,
                context={"request": request},
            )
            return self.get_paginated_response(serializer.data)

        serializer = PostListSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return self.success_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = PostDetailSerializer(
            self.get_object(),
            context={"request": request},
        )
        return self.success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return self.success_response(
            PostDetailSerializer(post, context={"request": request}).data,
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return self.success_response(
            PostDetailSerializer(post, context={"request": request}).data,
        )

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return APIResponse.empty()
