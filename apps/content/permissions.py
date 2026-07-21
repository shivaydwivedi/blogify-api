"""Permissions for content taxonomy APIs."""

from __future__ import annotations

from apps.common.permissions import BasePermission


class IsStaffOrReadOnly(BasePermission):
    """Allow public reads and restrict writes to staff or administrator users."""

    message = "Staff privileges are required to modify this resource."

    def has_permission(self, request, view) -> bool:
        if self.is_safe_method(request):
            return True

        return self.is_staff(request) or self.is_admin(request)
