"""Views for like APIs."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status

from apps.common.api import BaseAPIView
from apps.common.responses import APIResponse
from apps.likes.models import Like
from apps.likes.serializers import LikeSerializer
from apps.posts.models import Post, PostStatus


@extend_schema(tags=["Likes"])
class PostLikeAPIView(BaseAPIView):
    """Like or unlike a published post."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_post(self) -> Post:
        return get_object_or_404(Post.objects.all(), pk=self.kwargs["post_id"])

    @extend_schema(responses={200: OpenApiResponse(description="Post liked.")})
    def post(self, request, post_id):
        post = self.get_post()
        if post.status != PostStatus.PUBLISHED:
            return self.error_response(
                code="validation_error",
                message="Likes are only allowed on published posts.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        return self.success_response(
            {"liked": True, "like_count": post.likes.count(), "created": created},
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @extend_schema(responses={204: OpenApiResponse(description="Post unliked.")})
    def delete(self, request, post_id):
        post = self.get_post()
        Like.objects.filter(user=request.user, post=post).delete()
        return APIResponse.empty()
