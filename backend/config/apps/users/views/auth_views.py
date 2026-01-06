from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from config.apps.users.models.user import User
from config.apps.users.serializers.auth_serializers import LoginSerializer
from config.apps.users.services.jwt_service import create_access_token


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = User.objects(username=username, is_active=True).first()

        if not user or not user.check_password(password):
            return Response(
                {"detail": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = create_access_token(user)

        return Response(
            {
                "access_token": token,
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "rol": user.rol,
                }
            },
            status=status.HTTP_200_OK
        )
