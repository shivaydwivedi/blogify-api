"""Bookmark API routes."""

from __future__ import annotations

from django.urls import path

from apps.bookmarks.views import BookmarkListAPIView, PostBookmarkAPIView

app_name = "bookmarks"

urlpatterns = [
    path("bookmarks/", BookmarkListAPIView.as_view(), name="bookmark-list"),
    path(
        "posts/<uuid:post_id>/bookmark/",
        PostBookmarkAPIView.as_view(),
        name="post-bookmark",
    ),
]
