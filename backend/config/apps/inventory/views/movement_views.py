from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.movement import Movement
from config.apps.inventory.serializers.movement_serializer import MovementSerializer
from config.apps.users.permissions.movement_permissions import MovementPermission


class MovementListView(APIView):
    """
    GET -> Auditoría de movimientos (solo lectura)
    """
    permission_classes = [MovementPermission]

    def get(self, request):
        queryset = Movement.objects()

        # 🔹 Filtro por item
        item_id = request.query_params.get("item_id")
        if item_id:
            queryset = queryset.filter(item=item_id)

        # 🔹 Filtro por tipo
        tipo = request.query_params.get("tipo_movimiento")
        if tipo:
            queryset = queryset.filter(tipo_movimiento=tipo)

        serializer = MovementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
