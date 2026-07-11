"""Reusable abstract model foundations for Blogify API."""

from __future__ import annotations

import uuid
from typing import Any

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.managers import ActiveManager, AllObjectsManager, DeletedManager


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = ActiveManager()
    deleted_objects = DeletedManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def get_soft_delete_update_fields(self) -> list[str]:
        update_fields = ["is_deleted", "deleted_at"]
        model_field_names = {field.name for field in self._meta.fields}
        if "updated_at" in model_field_names:
            update_fields.append("updated_at")
        return update_fields

    def soft_delete(self, *, using: str | None = None) -> None:
        if self.is_deleted:
            return

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=self.get_soft_delete_update_fields())

    def restore(self, *, using: str | None = None) -> None:
        if not self.is_deleted:
            return

        self.is_deleted = False
        self.deleted_at = None
        self.save(using=using, update_fields=self.get_soft_delete_update_fields())

    def hard_delete(
        self,
        using: str | None = None,
        keep_parents: bool = False,
    ) -> tuple[int, dict[str, int]]:
        return super().delete(using=using, keep_parents=keep_parents)

    def delete(
        self,
        using: str | None = None,
        keep_parents: bool = False,
        **kwargs: Any,
    ) -> tuple[int, dict[str, int]]:
        hard = kwargs.pop("hard", False)
        if hard:
            return self.hard_delete(using=using, keep_parents=keep_parents)

        if self.is_deleted:
            return 0, {}

        self.soft_delete(using=using)
        return 1, {self._meta.label: 1}


class AuditModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimestampedModel, SoftDeleteModel, AuditModel):
    class Meta:
        abstract = True
        ordering = ("-created_at",)
