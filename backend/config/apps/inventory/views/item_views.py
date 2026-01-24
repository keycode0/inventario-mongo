from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.item import Item
from config.apps.inventory.serializers.item_serializer import ItemSerializer
from config.apps.inventory.services.item_service import ALLOWED_ITEM_STATES
from config.apps.users.permissions.item_permissions import ItemPermission


class ItemListCreateView(APIView):
    permission_classes = [ItemPermission]

    def get(self, request):
        queryset = Item.objects(is_active=True)

        # 🔹 filtro por estado
        estado = request.query_params.get("estado")
        if estado:
            if estado not in ALLOWED_ITEM_STATES:
                return Response(
                    {"detail": "Invalid estado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(estado=estado)

        # 🔹 filtro por subcategoría
        subcategoria_id = request.query_params.get("subcategoria_id")
        if subcategoria_id:
            try:
                queryset = queryset.filter(subcategoria_id=subcategoria_id)
            except Exception:
                return Response(
                    {"detail": "Invalid subcategoria_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemDetailView(APIView):
    permission_classes = [ItemPermission]

    def put(self, request, pk):
        try:
            item = Item.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid item id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not item:
            return Response(
                {"detail": "Item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ItemSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            item = Item.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid item id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not item:
            return Response(
                {"detail": "Item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        item.is_active = False
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
