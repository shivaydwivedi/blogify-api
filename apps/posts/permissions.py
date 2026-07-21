"""Permissions for post APIs."""

from __future__ import annotations

from apps.common.permissions import BasePermission
from apps.posts.models import PostStatus


class CanAccessPost(BasePermission):
    """Allow public reads for published posts and owner/staff management."""

    message = "You do not have permission to access this post."

    def has_permission(self, request, view) -> bool:
        if self.is_safe_method(request):
            return True

        return self.is_authenticated(request)

    def has_object_permission(self, request, view, obj) -> bool:
        if self.is_staff(request) or self.is_admin(request):
            return True

        if self.is_safe_method(request):
            if obj.status == PostStatus.PUBLISHED:
                return True
            return self.is_authenticated(request) and obj.author_id == request.user.id

        return self.is_authenticated(request) and obj.author_id == request.user.id
