"""Like API routes."""

from __future__ import annotations

from django.urls import path

from apps.likes.views import PostLikeAPIView

app_name = "likes"

urlpatterns = [
    path("posts/<uuid:post_id>/like/", PostLikeAPIView.as_view(), name="post-like"),
]
