"""Shared permission behavior."""

from __future__ import annotations

from apps.common.exceptions import ErrorCode
from apps.common.permissions.utils import (
    is_admin_user,
    is_authenticated_user,
    is_safe_method,
    is_staff_user,
    resolve_owner,
    user_owns_object,
)


class PermissionMixin:
    """Reusable helpers for class-based permission checks."""

    owner_attribute = "owner"
    message = "Permission denied."
    code = ErrorCode.PERMISSION_DENIED.value

    def get_error_code(self) -> str:
        """Return the stable API error code for this permission."""

        return self.code

    def get_user(self, request):
        """Return the requester associated with a DRF request-like object."""

        return getattr(request, "user", None)

    def is_safe_method(self, request) -> bool:
        """Return whether the request method is read-only."""

        return is_safe_method(getattr(request, "method", None))

    def is_authenticated(self, request) -> bool:
        """Return whether the requester is authenticated."""

        return is_authenticated_user(self.get_user(request))

    def is_staff(self, request) -> bool:
        """Return whether the requester has staff privileges."""

        return is_staff_user(self.get_user(request))

    def is_admin(self, request) -> bool:
        """Return whether the requester has administrator privileges."""

        return is_admin_user(self.get_user(request))

    def get_owner(self, obj):
        """Resolve the owner from an object using this permission's owner path."""

        return resolve_owner(obj, self.owner_attribute)

    def is_owner(self, request, obj) -> bool:
        """Return whether the requester owns the object."""

        return user_owns_object(
            self.get_user(request),
            obj,
            owner_attribute=self.owner_attribute,
        )
