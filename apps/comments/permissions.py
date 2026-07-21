"""Permissions for comment APIs."""

from __future__ import annotations

from apps.common.permissions import BasePermission


class CanManageComment(BasePermission):
    """Allow public reads and restrict writes to owners or staff."""

    message = "You do not have permission to manage this comment."

    def has_permission(self, request, view) -> bool:
        if self.is_safe_method(request):
            return True

        return self.is_authenticated(request)

    def has_object_permission(self, request, view, obj) -> bool:
        if self.is_safe_method(request):
            return True

        if self.is_staff(request) or self.is_admin(request):
            return True

        return self.is_authenticated(request) and obj.author_id == request.user.id
