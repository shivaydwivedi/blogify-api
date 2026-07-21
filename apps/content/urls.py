"""Content taxonomy API routes."""

from __future__ import annotations

from rest_framework.routers import SimpleRouter

from apps.content.views import CategoryViewSet, TagViewSet

app_name = "content"

router = SimpleRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = router.urls
