"""Generic permission utility functions."""

from __future__ import annotations

from typing import Any

from rest_framework.permissions import SAFE_METHODS


def is_safe_method(method: str | None) -> bool:
    """Return whether an HTTP method is read-only."""

    return method in SAFE_METHODS


def is_authenticated_user(user: Any) -> bool:
    """Return whether a user-like object represents an authenticated requester."""

    return bool(user and getattr(user, "is_authenticated", False))


def is_staff_user(user: Any) -> bool:
    """Return whether a user-like object has staff privileges."""

    return bool(is_authenticated_user(user) and getattr(user, "is_staff", False))


def is_admin_user(user: Any) -> bool:
    """Return whether a user-like object has administrator privileges."""

    return bool(is_authenticated_user(user) and getattr(user, "is_superuser", False))


def get_attribute(obj: Any, attribute_path: str, default: Any = None) -> Any:
    """Resolve a dotted attribute path from an object."""

    current = obj

    for attribute in attribute_path.split("."):
        if current is None:
            return default

        current = getattr(current, attribute, default)

    return current


def resolve_owner(obj: Any, owner_attribute: str = "owner") -> Any:
    """Resolve the owner of an object using a configurable attribute path."""

    return get_attribute(obj, owner_attribute)


def user_owns_object(user: Any, obj: Any, owner_attribute: str = "owner") -> bool:
    """Return whether a user-like object owns an object."""

    if not is_authenticated_user(user):
        return False

    owner = resolve_owner(obj, owner_attribute)

    if owner is None:
        return False

    return owner == user
