"""Core operational routes."""

from __future__ import annotations

from django.urls import path

from apps.core.views import HealthCheckAPIView

app_name = "core"

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view(), name="health"),
]
