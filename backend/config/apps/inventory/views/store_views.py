from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.store import Store
from config.apps.inventory.serializers.store_serializer import StoreSerializer
from config.apps.users.permissions.store_permissions import StorePermission


class StoreListCreateView(APIView):
    permission_classes = [StorePermission]

    def get(self, request):
        stores = Store.objects(activo=True)
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StoreDetailView(APIView):
    permission_classes = [StorePermission]

    def put(self, request, pk):
        try:
            store = Store.objects(id=pk, activo=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid store id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not store:
            return Response(
                {"detail": "Store not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StoreSerializer(store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            store = Store.objects(id=pk, activo=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid store id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not store:
            return Response(
                {"detail": "Store not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        store.activo = False
        store.save()
        return Response(
            {"detail": "Store deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
