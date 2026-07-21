"""Account authentication routes."""

from __future__ import annotations

from django.urls import path

from apps.accounts.views import (
    ChangePasswordAPIView,
    CurrentUserAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshTokenAPIView,
    RegisterAPIView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("me/", CurrentUserAPIView.as_view(), name="me"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
]
