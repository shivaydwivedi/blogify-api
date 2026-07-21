"""Comment API routes."""

from __future__ import annotations

from django.urls import path

from apps.comments.views import CommentDetailAPIView, PostCommentListCreateAPIView

app_name = "comments"

urlpatterns = [
    path(
        "posts/<uuid:post_id>/comments/",
        PostCommentListCreateAPIView.as_view(),
        name="post-comments",
    ),
    path("comments/<uuid:pk>/", CommentDetailAPIView.as_view(), name="comment-detail"),
]
