from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.customer import Customer
from config.apps.inventory.serializers.customer_serializer import CustomerSerializer
from config.apps.users.permissions.inventory_permissions import InventoryPermission


class CustomerListCreateView(APIView):
    permission_classes = [InventoryPermission]
    resource_name = "customer"

    def get(self, request):
        customers = Customer.objects(is_active=True)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomerDetailView(APIView):
    permission_classes = [InventoryPermission]
    resource_name = "customer"

    def put(self, request, pk):
        try:
            customer = Customer.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid customer id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not customer:
            return Response(
                {"detail": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            customer = Customer.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid customer id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not customer:
            return Response(
                {"detail": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        customer.is_active = False
        customer.save()
        return Response(
            {"detail": "Customer deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
