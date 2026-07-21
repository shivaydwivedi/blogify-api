"""Base permission primitives."""

from __future__ import annotations

from rest_framework.permissions import BasePermission as DRFBasePermission

from apps.common.exceptions import ErrorCode
from apps.common.permissions.mixins import PermissionMixin


class BasePermission(PermissionMixin, DRFBasePermission):
    """Base class for reusable project permissions."""

    message = "Permission denied."
    code = ErrorCode.PERMISSION_DENIED.value

    def has_permission(self, request, view) -> bool:
        """Allow by default so subclasses can define only the checks they need."""

        return True

    def has_object_permission(self, request, view, obj) -> bool:
        """Allow by default so object-aware subclasses remain explicit."""

        return True
