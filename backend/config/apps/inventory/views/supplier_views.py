from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.supplier import Supplier
from config.apps.inventory.serializers.supplier_serializer import SupplierSerializer
from config.apps.users.permissions.inventory_permissions import InventoryPermission


class SupplierListCreateView(APIView):
    permission_classes = [InventoryPermission]
    resource_name = "supplier"

    def get(self, request):
        suppliers = Supplier.objects(is_active=True)
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupplierDetailView(APIView):
    permission_classes = [InventoryPermission]
    resource_name = "supplier"

    def put(self, request, pk):
        try:
            supplier = Supplier.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid supplier id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not supplier:
            return Response(
                {"detail": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            supplier = Supplier.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid supplier id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not supplier:
            return Response(
                {"detail": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        supplier.is_active = False
        supplier.save()
        return Response(
            {"detail": "Supplier deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
