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
        # 1️⃣ Validar datos de entrada
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # 2️⃣ Buscar usuario en MongoDB
        user = User.objects(username=username).first()

        # 3️⃣ Validar credenciales
        if not user or not user.check_password(password):
            return Response(
                {"detail": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 4️⃣ Generar token JWT (PROTEGIDO)
        try:
            token = create_access_token(user)
        except Exception as e:
            # ⚠️ Evita socket hang up y muestra el error real
            return Response(
                {
                    "detail": "Error al generar el token",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 5️⃣ Respuesta exitosa
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
