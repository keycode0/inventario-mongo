from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.item import Item
from config.apps.inventory.serializers.item_serializer import ItemSerializer
from config.apps.users.permissions.item_permissions import ItemPermission


class ItemListCreateView(APIView):
    permission_classes = [ItemPermission]

    def get(self, request):
        items = Item.objects(is_active=True)
        serializer = ItemSerializer(items, many=True)
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
