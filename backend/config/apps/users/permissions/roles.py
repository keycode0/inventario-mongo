from enum import Enum
from rest_framework.permissions import BasePermission


class Roles(str, Enum):
    ADMIN = "admin"
    TECNICO = "tecnico"
    ADMINISTRATIVO = "administrativo"


class RolePermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_active:
            return False
        return user.rol in self.allowed_roles


class AdminOnly(RolePermission):
    allowed_roles = [Roles.ADMIN.value]


class AdminOrTecnico(RolePermission):
    allowed_roles = [
        Roles.ADMIN.value,
        Roles.TECNICO.value,
    ]
