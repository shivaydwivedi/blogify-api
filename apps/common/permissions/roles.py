"""Reusable role-based permissions."""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to administrator users."""

    message = "Administrator privileges are required."

    def has_permission(self, request, view) -> bool:
        return self.is_admin(request)

    def has_object_permission(self, request, view, obj) -> bool:
        return self.is_admin(request)


class IsStaff(BasePermission):
    """Allow access only to staff users."""

    message = "Staff privileges are required."

    def has_permission(self, request, view) -> bool:
        return self.is_staff(request)

    def has_object_permission(self, request, view, obj) -> bool:
        return self.is_staff(request)
