"""Notification API routes."""

from __future__ import annotations

from django.urls import path

from apps.notifications.views import (
    NotificationListAPIView,
    NotificationReadAllAPIView,
    NotificationReadAPIView,
)

app_name = "notifications"

urlpatterns = [
    path("notifications/", NotificationListAPIView.as_view(), name="notification-list"),
    path(
        "notifications/<uuid:pk>/read/",
        NotificationReadAPIView.as_view(),
        name="notification-read",
    ),
    path(
        "notifications/read-all/",
        NotificationReadAllAPIView.as_view(),
        name="notification-read-all",
    ),
]
