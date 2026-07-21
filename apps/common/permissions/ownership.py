"""Reusable ownership-based permissions."""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class IsOwner(BasePermission):
    """Allow access only to the authenticated owner of an object."""

    message = "Only the resource owner may perform this action."

    def has_object_permission(self, request, view, obj) -> bool:
        return self.is_owner(request, obj)


class IsOwnerOrReadOnly(BasePermission):
    """Allow read access to all requesters and write access to object owners."""

    message = "Only the resource owner may modify this resource."

    def has_object_permission(self, request, view, obj) -> bool:
        if self.is_safe_method(request):
            return True

        return self.is_owner(request, obj)
