"""Account domain models."""

from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone

from apps.accounts.managers import UserManager
from apps.common.models import UUIDModel


class User(UUIDModel, AbstractBaseUser, PermissionsMixin):
    """Custom account identity model for Blogify API."""

    email = models.EmailField(
        unique=True,
        validators=(EmailValidator(),),
        error_messages={"unique": "A user with this email already exists."},
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        error_messages={"unique": "A user with this username already exists."},
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ("email",)
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self) -> None:
        super().clean()
        self.email = User.objects.normalize_email(self.email)

    def save(self, *args, **kwargs) -> None:
        self.email = User.objects.normalize_email(self.email)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email
