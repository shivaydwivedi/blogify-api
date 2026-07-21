from __future__ import annotations

from types import SimpleNamespace

from apps.common.api import BasePermission as APIBasePermission
from apps.common.permissions import (
    BasePermission,
    IsAdmin,
    IsOwner,
    IsOwnerOrReadOnly,
    IsStaff,
    PermissionMixin,
    get_attribute,
    is_admin_user,
    is_authenticated_user,
    is_safe_method,
    is_staff_user,
    resolve_owner,
    user_owns_object,
)


def build_user(
    *,
    user_id: int,
    is_authenticated: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
):
    return SimpleNamespace(
        id=user_id,
        is_authenticated=is_authenticated,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )


def build_request(method: str, user=None):
    return SimpleNamespace(method=method, user=user)


def test_permission_framework_imports() -> None:
    assert APIBasePermission is BasePermission
    assert issubclass(IsOwner, BasePermission)
    assert issubclass(IsOwnerOrReadOnly, BasePermission)
    assert issubclass(IsAdmin, BasePermission)
    assert issubclass(IsStaff, BasePermission)


def test_base_permission_exposes_stable_error_code() -> None:
    permission = BasePermission()

    assert permission.get_error_code() == "permission_denied"


def test_permission_utilities_identify_safe_methods() -> None:
    assert is_safe_method("GET") is True
    assert is_safe_method("HEAD") is True
    assert is_safe_method("OPTIONS") is True
    assert is_safe_method("POST") is False


def test_permission_utilities_identify_authenticated_staff_and_admin_users() -> None:
    anonymous = build_user(user_id=1, is_authenticated=False)
    staff = build_user(user_id=2, is_staff=True)
    admin = build_user(user_id=3, is_superuser=True)

    assert is_authenticated_user(anonymous) is False
    assert is_authenticated_user(staff) is True
    assert is_staff_user(staff) is True
    assert is_staff_user(admin) is False
    assert is_admin_user(staff) is False
    assert is_admin_user(admin) is True


def test_get_attribute_resolves_nested_paths() -> None:
    owner = build_user(user_id=1)
    obj = SimpleNamespace(author=SimpleNamespace(user=owner))

    assert get_attribute(obj, "author.user") == owner
    assert get_attribute(obj, "author.profile", default="missing") == "missing"
    assert get_attribute(None, "author.user", default="missing") == "missing"


def test_resolve_owner_uses_configurable_owner_attribute() -> None:
    owner = build_user(user_id=1)
    obj = SimpleNamespace(author=SimpleNamespace(user=owner))

    assert resolve_owner(obj, "author.user") == owner
    assert resolve_owner(obj, "owner") is None


def test_user_owns_object_requires_authenticated_matching_owner() -> None:
    owner = build_user(user_id=1)
    other_user = build_user(user_id=2)
    anonymous = build_user(user_id=3, is_authenticated=False)
    obj = SimpleNamespace(owner=owner)

    assert user_owns_object(owner, obj) is True
    assert user_owns_object(other_user, obj) is False
    assert user_owns_object(anonymous, obj) is False
    assert user_owns_object(owner, SimpleNamespace()) is False


def test_is_owner_allows_only_authenticated_object_owner() -> None:
    owner = build_user(user_id=1)
    other_user = build_user(user_id=2)
    obj = SimpleNamespace(owner=owner)
    permission = IsOwner()

    assert permission.has_object_permission(build_request("PATCH", owner), None, obj)
    assert not permission.has_object_permission(
        build_request("PATCH", other_user),
        None,
        obj,
    )


def test_is_owner_or_read_only_allows_safe_methods_for_any_requester() -> None:
    owner = build_user(user_id=1)
    other_user = build_user(user_id=2)
    obj = SimpleNamespace(owner=owner)
    permission = IsOwnerOrReadOnly()

    assert permission.has_object_permission(build_request("GET", None), None, obj)
    assert permission.has_object_permission(
        build_request("HEAD", other_user), None, obj
    )
    assert permission.has_object_permission(build_request("PATCH", owner), None, obj)
    assert not permission.has_object_permission(
        build_request("PATCH", other_user),
        None,
        obj,
    )


def test_role_permissions_are_explicit() -> None:
    staff = build_user(user_id=1, is_staff=True)
    admin = build_user(user_id=2, is_superuser=True)
    standard_user = build_user(user_id=3)

    assert IsStaff().has_permission(build_request("GET", staff), None)
    assert not IsStaff().has_permission(build_request("GET", admin), None)
    assert IsAdmin().has_permission(build_request("GET", admin), None)
    assert not IsAdmin().has_permission(build_request("GET", staff), None)
    assert not IsAdmin().has_permission(build_request("GET", standard_user), None)


def test_permission_mixin_supports_nested_owner_paths() -> None:
    class NestedOwnerPermission(PermissionMixin):
        owner_attribute = "author.user"

    owner = build_user(user_id=1)
    obj = SimpleNamespace(author=SimpleNamespace(user=owner))
    permission = NestedOwnerPermission()

    assert permission.get_owner(obj) == owner
    assert permission.is_owner(build_request("PUT", owner), obj)
