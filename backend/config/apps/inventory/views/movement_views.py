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
        queryset = Movement.objects()

        item_id = request.query_params.get("item_id")
        if item_id:
            queryset = queryset.filter(item=item_id)

        tipo = request.query_params.get("tipo_movimiento")
        if tipo:
            queryset = queryset.filter(tipo_movimiento=tipo)

        serializer = MovementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MovementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movement = register_movement(**serializer.validated_data)

        return Response(
            MovementSerializer(movement).data,
            status=status.HTTP_201_CREATED
        )
