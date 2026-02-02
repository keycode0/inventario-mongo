from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.facility import Facility
from config.apps.inventory.serializers.facility_detail_serializer import (
    FacilityDetailSerializer
)
from config.apps.users.permissions.role_permissions import AdminOrTecnico


class FacilityEnrichedDetailView(APIView):
    permission_classes = [AdminOrTecnico]

    def get(self, request, pk):
        facility = Facility.objects(id=pk, is_active=True).first()

        if not facility:
            return Response(
                {"detail": "Instalación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FacilityDetailSerializer(facility)
        return Response(serializer.data, status=status.HTTP_200_OK)
