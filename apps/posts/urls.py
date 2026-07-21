"""Post API routes."""

from __future__ import annotations

from rest_framework.routers import SimpleRouter

from apps.posts.views import PostViewSet

app_name = "posts"

router = SimpleRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = router.urls
