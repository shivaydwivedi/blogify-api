"""Reusable permission framework."""

from apps.common.permissions.base import BasePermission
from apps.common.permissions.mixins import PermissionMixin
from apps.common.permissions.ownership import IsOwner, IsOwnerOrReadOnly
from apps.common.permissions.roles import IsAdmin, IsStaff
from apps.common.permissions.utils import (
    get_attribute,
    is_admin_user,
    is_authenticated_user,
    is_safe_method,
    is_staff_user,
    resolve_owner,
    user_owns_object,
)

__all__ = (
    "BasePermission",
    "IsAdmin",
    "IsOwner",
    "IsOwnerOrReadOnly",
    "IsStaff",
    "PermissionMixin",
    "get_attribute",
    "is_admin_user",
    "is_authenticated_user",
    "is_safe_method",
    "is_staff_user",
    "resolve_owner",
    "user_owns_object",
)
