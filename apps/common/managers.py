"""Reusable model managers for shared lifecycle behavior."""

from __future__ import annotations

from django.db import models


class ActiveManager(models.Manager):
    """Return records that are not soft-deleted."""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class DeletedManager(models.Manager):
    """Return records that have been soft-deleted."""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=True)


class AllObjectsManager(models.Manager):
    """Return records without applying soft-delete filtering."""
