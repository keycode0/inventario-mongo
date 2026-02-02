from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.users.models.user import User
from config.apps.users.permissions.role_permissions import AdminOnly


class UserListView(APIView):
    """
    GET /users/
    Lista todos los usuarios activos.
    SOLO ADMIN
    """

    permission_classes = [AdminOnly]

    def get(self, request):
        users = User.objects(is_active=True)

        data = [
            {
                "id": str(u.id),
                "username": u.username,
                "rol": u.rol,
            }
            for u in users
        ]

        return Response(data, status=status.HTTP_200_OK)
