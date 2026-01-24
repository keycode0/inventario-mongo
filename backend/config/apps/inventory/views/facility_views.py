from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.facility import Facility
from config.apps.inventory.serializers.facility_serializer import FacilitySerializer
from config.apps.inventory.services.facility_service import (
    soft_delete_facility,
    ALLOWED_FACILITY_STATES,
)
from config.apps.users.permissions.facility_permissions import FacilityPermission
from config.apps.users.models.user import User

class FacilityListCreateView(APIView):
    """
    GET  -> Listar instalaciones activas
    POST -> Crear instalación
    """
    permission_classes = [FacilityPermission]

    def get(self, request):
        queryset = Facility.objects(is_active=True)

        # 🔹 Filtro por estado
        estado = request.query_params.get("estado")
        if estado:
            if estado not in ALLOWED_FACILITY_STATES:
                return Response(
                    {"detail": "Invalid estado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(estado=estado)

        # 🔹 Filtro por técnico
        tecnico_id = request.query_params.get("tecnico_id")
        if tecnico_id:
            try:
                tecnico = User.objects(
                    id=tecnico_id,
                    is_active=True,
                    rol="tecnico"
                ).first()
            except Exception:
                return Response(
                    {"detail": "Invalid tecnico_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not tecnico:
                return Response(
                    {"detail": "Tecnico not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            queryset = queryset.filter(tecnico_id=tecnico)

        serializer = FacilitySerializer(queryset, many=True)
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
