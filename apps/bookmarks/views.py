"""Views for bookmark APIs."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status

from apps.bookmarks.models import Bookmark
from apps.bookmarks.serializers import BookmarkSerializer
from apps.common.api import BaseAPIView, BasePagination
from apps.common.responses import APIResponse
from apps.posts.models import Post, PostStatus


@extend_schema(tags=["Bookmarks"])
class BookmarkListAPIView(BaseAPIView):
    """List the authenticated user's bookmarked posts."""

    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BasePagination
    serializer_class = BookmarkSerializer

    def get(self, request):
        queryset = (
            Bookmark.objects.filter(
                user=request.user, post__status=PostStatus.PUBLISHED
            )
            .select_related("post", "post__author", "post__category")
            .prefetch_related("post__tags")
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = BookmarkSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


@extend_schema(tags=["Bookmarks"])
class PostBookmarkAPIView(BaseAPIView):
    """Bookmark or remove a bookmark from a published post."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BookmarkSerializer

    def get_post(self) -> Post:
        return get_object_or_404(Post.objects.all(), pk=self.kwargs["post_id"])

    @extend_schema(responses={200: OpenApiResponse(description="Post bookmarked.")})
    def post(self, request, post_id):
        post = self.get_post()
        if post.status != PostStatus.PUBLISHED:
            return self.error_response(
                code="validation_error",
                message="Bookmarks are only allowed on published posts.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        return self.success_response(
            {"bookmarked": True, "created": created},
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @extend_schema(responses={204: OpenApiResponse(description="Bookmark removed.")})
    def delete(self, request, post_id):
        post = self.get_post()
        Bookmark.objects.filter(user=request.user, post=post).delete()
        return APIResponse.empty()
