"""Views for comment APIs."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status

from apps.comments.models import Comment
from apps.comments.permissions import CanManageComment
from apps.comments.serializers import CommentSerializer, CommentUpdateSerializer
from apps.common.api import BaseAPIView, BasePagination
from apps.common.responses import APIResponse
from apps.posts.models import Post, PostStatus


@extend_schema(tags=["Comments"])
class PostCommentListCreateAPIView(BaseAPIView):
    """List comments for a post or add a new comment."""

    permission_classes = (CanManageComment,)
    pagination_class = BasePagination
    serializer_class = CommentSerializer

    def get_post(self) -> Post:
        return get_object_or_404(Post.objects.all(), pk=self.kwargs["post_id"])

    def get(self, request, post_id):
        post = get_object_or_404(
            Post.objects.all(), pk=post_id, status=PostStatus.PUBLISHED
        )
        queryset = (
            Comment.objects.filter(post=post, parent__isnull=True)
            .select_related("author", "post")
            .prefetch_related("replies__author")
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = CommentSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(request=CommentSerializer, responses={201: CommentSerializer})
    def post(self, request, post_id):
        post = self.get_post()
        serializer = CommentSerializer(
            data=request.data,
            context={"request": request, "post": post},
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return self.success_response(
            CommentSerializer(comment, context={"request": request}).data,
            status_code=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Comments"])
class CommentDetailAPIView(BaseAPIView):
    """Update or delete a comment."""

    permission_classes = (CanManageComment,)
    serializer_class = CommentUpdateSerializer

    def get_object(self) -> Comment:
        comment = get_object_or_404(
            Comment.objects.select_related("author", "post"),
            pk=self.kwargs["pk"],
        )
        self.check_object_permissions(self.request, comment)
        return comment

    @extend_schema(request=CommentUpdateSerializer, responses={200: CommentSerializer})
    def put(self, request, pk):
        return self.update(request, pk)

    @extend_schema(request=CommentUpdateSerializer, responses={200: CommentSerializer})
    def patch(self, request, pk):
        return self.update(request, pk)

    def update(self, request, pk):
        comment = self.get_object()
        serializer = CommentUpdateSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return self.success_response(
            CommentSerializer(comment, context={"request": request}).data,
        )

    def delete(self, request, pk):
        self.get_object().delete()
        return APIResponse.empty()
