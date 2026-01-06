from rest_framework.permissions import BasePermission, SAFE_METHODS
from config.apps.users.permissions.permissions_map import ROLE_PERMISSIONS


class InventoryPermission(BasePermission):
    """
    Permisos CRUD para items.
    DELETE = soft delete
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)

        if not user or not user.is_active:
            return False

        role_permissions = ROLE_PERMISSIONS.get(user.rol, set())

        if request.method in SAFE_METHODS:
            return "items:read" in role_permissions

        if request.method == "POST":
            return "items:create" in role_permissions

        if request.method in ("PUT", "PATCH"):
            return "items:update" in role_permissions

        if request.method == "DELETE":
            return "items:delete" in role_permissions

        return False
