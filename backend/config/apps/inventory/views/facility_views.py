from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.facility import Facility
from config.apps.inventory.serializers.facility_serializer import FacilitySerializer
from config.apps.inventory.services.facility_service import soft_delete_facility
from config.apps.users.permissions.facility_permissions import FacilityPermission

class FacilityListCreateView(APIView):
    """
    GET  -> Listar instalaciones activas
    POST -> Crear instalación
    """
    permission_classes = [FacilityPermission]

    def get(self, request):
        facilities = Facility.objects(is_active=True)
        serializer = FacilitySerializer(facilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FacilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FacilityDetailView(APIView):
    """
    PUT    -> Actualizar instalación
    DELETE -> Eliminación lógica (service)
    """
    permission_classes = [FacilityPermission]

    def put(self, request, pk):
        facility = Facility.objects(id=pk, is_active=True).first()
        if not facility:
            return Response(
                {"detail": "Instalación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FacilitySerializer(facility, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        facility = Facility.objects(id=pk, is_active=True).first()
        if not facility:
            return Response(
                {"detail": "Instalación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        soft_delete_facility(facility)
        return Response(status=status.HTTP_204_NO_CONTENT)
