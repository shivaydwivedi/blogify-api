"""Authentication API views for the account domain."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core import signing
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from apps.accounts.tasks import send_verification_email
from apps.accounts.tokens import load_email_verification_token
from apps.common.api import BaseAPIView
from apps.common.responses import APIResponse

User = get_user_model()


def build_token_payload(user) -> dict[str, str]:
    """Build access and refresh tokens for an authenticated user."""

    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class RegisterAPIView(BaseAPIView):
    """Register a new user account."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @extend_schema(
        request=RegisterSerializer,
        responses={201: OpenApiResponse(response=UserSerializer)},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email.delay(str(user.id))

        return self.success_response(
            UserSerializer(user, context={"request": request}).data,
            status_code=status.HTTP_201_CREATED,
        )


class LoginAPIView(BaseAPIView):
    """Authenticate a user and issue JWT tokens."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiResponse(description="JWT token pair issued.")},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        return self.success_response(
            {
                "tokens": build_token_payload(user),
                "user": UserSerializer(user, context={"request": request}).data,
            },
        )


class RefreshTokenAPIView(BaseAPIView):
    """Refresh a JWT token pair."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenRefreshSerializer

    @extend_schema(
        request=TokenRefreshSerializer,
        responses={200: OpenApiResponse(description="JWT token refreshed.")},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return self.success_response({"tokens": serializer.validated_data})


class LogoutAPIView(BaseAPIView):
    """Blacklist a refresh token."""

    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {"refresh": {"type": "string"}},
                "required": ["refresh"],
            }
        },
        responses={204: OpenApiResponse(description="Refresh token blacklisted.")},
        tags=["Authentication"],
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return self.error_response(
                code="validation_error",
                message="Invalid request.",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"refresh": ["This field is required."]},
            )

        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return self.error_response(
                code="validation_error",
                message="Invalid refresh token.",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"refresh": ["Token is invalid or expired."]},
            )

        return APIResponse.empty()


class CurrentUserAPIView(BaseAPIView):
    """Return the authenticated user's account context."""

    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        responses={200: UserSerializer},
        tags=["Authentication"],
    )
    def get(self, request):
        return self.success_response(
            UserSerializer(request.user, context={"request": request}).data,
        )


class ChangePasswordAPIView(BaseAPIView):
    """Change the authenticated user's password."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: OpenApiResponse(description="Password changed.")},
        tags=["Authentication"],
    )
    def put(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.success_response({"detail": "Password changed successfully."})


class ResendVerificationAPIView(BaseAPIView):
    """Queue another verification email for the authenticated user."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(description="Verification email queued.")},
        tags=["Authentication"],
    )
    def post(self, request):
        if request.user.email_verified:
            return self.success_response({"detail": "Email is already verified."})

        send_verification_email.delay(str(request.user.id))
        return self.success_response({"detail": "Verification email queued."})


class VerifyEmailAPIView(BaseAPIView):
    """Verify a user's email address using a signed token."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    @extend_schema(
        parameters=[],
        responses={200: OpenApiResponse(description="Email verified.")},
        tags=["Authentication"],
    )
    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return self.error_response(
                code="validation_error",
                message="Verification token is required.",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"token": ["This query parameter is required."]},
            )

        try:
            payload = load_email_verification_token(token)
        except signing.SignatureExpired:
            return self.error_response(
                code="validation_error",
                message="Verification token has expired.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except signing.BadSignature:
            return self.error_response(
                code="validation_error",
                message="Verification token is invalid.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(
            pk=payload.get("user_id"),
            email=payload.get("email"),
        ).first()
        if user is None or user.email_verified:
            return self.error_response(
                code="validation_error",
                message="Verification token is invalid.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user.email_verified = True
        user.save(update_fields=("email_verified",))

        from apps.notifications.services import create_email_verified_notification

        create_email_verified_notification(user)
        return self.success_response({"detail": "Email verified successfully."})
