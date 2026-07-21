"""Serializers for account authentication workflows."""

from __future__ import annotations

from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Expose safe account identity fields."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "email_verified",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
        )
        read_only_fields = fields


class RegisterSerializer(serializers.Serializer):
    """Validate registration input and create a user account."""

    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate_email(self, value: str) -> str:
        email = BaseUserManager.normalize_email(value)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        try:
            password_validation.validate_password(attrs["password"])
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)}) from exc

        return attrs

    def create(self, validated_data: dict):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    """Validate credentials for token issuance."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    default_error_messages = {
        "invalid_credentials": "Unable to log in with the provided credentials.",
        "inactive": "This account is inactive.",
    }

    def validate(self, attrs: dict) -> dict:
        email = BaseUserManager.normalize_email(attrs["email"])
        password = attrs["password"]
        request = self.context.get("request")
        user = authenticate(request=request, username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                self.error_messages["invalid_credentials"],
                code="invalid_credentials",
            )

        if not user.is_active:
            raise serializers.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Validate password change requests for authenticated users."""

    current_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_current_password(self, value: str) -> str:
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Passwords do not match."}
            )

        try:
            password_validation.validate_password(
                attrs["new_password"],
                self.context["request"].user,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {"new_password": list(exc.messages)}
            ) from exc

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=("password",))
        return user
