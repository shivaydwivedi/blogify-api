"""Admin registration for account domain models."""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.accounts.forms import UserChangeForm, UserCreationForm
from apps.accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Admin configuration for the custom user model."""

    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "email_verified",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "email_verified",
        "groups",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
    readonly_fields = ("id", "last_login", "date_joined")
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("id", "email", "username", "password")}),
        (
            "Profile",
            {"fields": ("first_name", "last_name", "bio", "avatar")},
        ),
        (
            "Status",
            {"fields": ("email_verified", "is_active", "is_staff", "is_superuser")},
        ),
        (
            "Permissions",
            {"fields": ("groups", "user_permissions")},
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
