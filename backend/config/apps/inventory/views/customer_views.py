from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.customer import Customer
from config.apps.inventory.serializers.customer_serializer import CustomerSerializer
from config.apps.users.permissions.permissions_map import ROLE_PERMISSIONS


class CustomerListCreateView(APIView):
    """
    GET  /customers/   -> listar clientes
    POST /customers/   -> crear cliente
    """

    def get(self, request):
        user = request.user
        role_permissions = ROLE_PERMISSIONS.get(user.rol, set())

        if "customer:read" not in role_permissions:
            return Response(
                {"detail": "No tiene permiso para ver clientes"},
                status=status.HTTP_403_FORBIDDEN,
            )

        customers = Customer.objects(is_active=True)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        role_permissions = ROLE_PERMISSIONS.get(user.rol, set())

        if "customer:create" not in role_permissions:
            return Response(
                {"detail": "No tiene permiso para crear clientes"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        return Response(
            {"id": str(customer.id)},
            status=status.HTTP_201_CREATED,
        )


class CustomerDetailView(APIView):
    """
    PUT    /customers/<id>/   -> actualizar cliente
    DELETE /customers/<id>/   -> soft delete
    """

    def put(self, request, pk):
        user = request.user
        role_permissions = ROLE_PERMISSIONS.get(user.rol, set())

        if "customer:update" not in role_permissions:
            return Response(
                {"detail": "No tiene permiso para actualizar clientes"},
                status=status.HTTP_403_FORBIDDEN,
            )

        customer = Customer.objects(id=pk, is_active=True).first()
        if not customer:
            return Response(
                {"detail": "Cliente no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CustomerSerializer(
            customer, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = request.user
        role_permissions = ROLE_PERMISSIONS.get(user.rol, set())

        if "customer:delete" not in role_permissions:
            return Response(
                {"detail": "No tiene permiso para eliminar clientes"},
                status=status.HTTP_403_FORBIDDEN,
            )

        customer = Customer.objects(id=pk, is_active=True).first()
        if not customer:
            return Response(
                {"detail": "Cliente no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        customer.delete()  # soft delete

        return Response(
            {"detail": "Cliente eliminado correctamente"},
            status=status.HTTP_200_OK,
        )
