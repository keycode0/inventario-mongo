from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.movement import Movement
from config.apps.inventory.serializers.movement_serializer import MovementSerializer
from config.apps.inventory.services.movement_service import register_movement
from config.apps.users.permissions.movement_permissions import MovementPermission


class MovementListCreateView(APIView):
    """
    GET  -> Listar movimientos
    POST -> Registrar movimiento de inventario
    """
    permission_classes = [MovementPermission]

    def get(self, request):
        movements = Movement.objects()
        serializer = MovementSerializer(movements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MovementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movement = register_movement(**serializer.validated_data)

        return Response(
            MovementSerializer(movement).data,
            status=status.HTTP_201_CREATED
        )
