from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.users.models.user import User
from config.apps.users.permissions.role_permissions import AdminOnly
from config.apps.users.serializers.user_update_serializer import (
    UserUpdateSerializer,
)


class UserDetailView(APIView):
    """
    PUT    /users/<id>/   -> actualizar usuario
    DELETE /users/<id>/   -> soft delete usuario

    SOLO ADMIN
    """

    permission_classes = [AdminOnly]

    def get_object(self, pk):
        return User.objects(id=pk, is_active=True).first()

    # -------------------------
    # UPDATE
    # -------------------------
    def put(self, request, pk):
        user = self.get_object(pk)

        if not user:
            return Response(
                {"detail": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserUpdateSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "id": str(user.id),
                "username": user.username,
                "rol": user.rol,
            },
            status=status.HTTP_200_OK,
        )

    # -------------------------
    # DELETE (SOFT DELETE)
    # -------------------------
    def delete(self, request, pk):
        user = self.get_object(pk)

        if not user:
            return Response(
                {"detail": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 🔒 Admin NO puede eliminarse a sí mismo
        if str(user.id) == str(request.user.id):
            return Response(
                {"detail": "No puede eliminar su propio usuario"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔒 Nunca eliminar admin
        if user.rol == "admin":
            return Response(
                {"detail": "No se puede eliminar el usuario administrador"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.delete()  # soft delete

        return Response(
            {"detail": "Usuario eliminado correctamente"},
            status=status.HTTP_200_OK,
        )
