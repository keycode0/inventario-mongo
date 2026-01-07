from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.vehicle import Vehicle
from config.apps.inventory.serializers.vehicle_serializer import VehicleSerializer
from config.apps.users.permissions.inventory_permissions import InventoryPermission


class VehicleListCreateView(APIView):
    permission_classes = [InventoryPermission]
    resource_name = "vehicle"

    def get(self, request):
        vehicles = Vehicle.objects(is_active=True)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VehicleDetailView(APIView):
    permission_classes = [InventoryPermission]
    resource_name = "vehicle"

    def put(self, request, pk):
        try:
            vehicle = Vehicle.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid vehicle id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not vehicle:
            return Response(
                {"detail": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            vehicle = Vehicle.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid vehicle id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not vehicle:
            return Response(
                {"detail": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        vehicle.is_active = False
        vehicle.save()
        return Response(
            {"detail": "Vehicle deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
