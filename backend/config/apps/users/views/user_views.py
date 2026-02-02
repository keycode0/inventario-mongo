from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.users.models.user import User
from config.apps.users.permissions.role_permissions import (
    AdminOnly,
    AdminOrTecnico,
)
from config.apps.users.serializers.user_create_serializer import (
    UserCreateSerializer,
)


# ======================================================
# CREAR USUARIOS (SOLO ADMIN)
# ======================================================
class UserCreateView(APIView):
    """
    Permite crear usuarios (admin, tecnico, administrativo).
    SOLO accesible para rol admin.
    """
    permission_classes = [AdminOnly]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": str(user.id),
                "username": user.username,
                "rol": user.rol,
            },
            status=status.HTTP_201_CREATED,
        )


# ======================================================
# LISTAR TECNICOS (ADMIN Y TECNICO)
# ======================================================
class TechnicianListView(APIView):
    """
    Lista únicamente usuarios con rol = tecnico.
    Usado por el frontend para asignar técnicos a instalaciones.
    """
    permission_classes = [AdminOrTecnico]

    def get(self, request):
        technicians = User.objects(
            rol="tecnico",
            is_active=True,
        )

        data = [
            {
                "id": str(user.id),
                "username": user.username,
            }
            for user in technicians
        ]

        return Response(data, status=status.HTTP_200_OK)
