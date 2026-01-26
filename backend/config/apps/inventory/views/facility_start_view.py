from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.facility import Facility
from config.apps.inventory.services.facility_actions import (
    start_facility,
    FacilityActionError,
)
from config.apps.users.permissions.facility_permissions import FacilityPermission


class FacilityStartView(APIView):
    """
    POST -> Iniciar una instalación
    """
    permission_classes = [FacilityPermission]

    def post(self, request, pk):
        facility = Facility.objects(id=pk, is_active=True).first()
        if not facility:
            return Response(
                {"detail": "Instalación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        # Seguridad: técnico asignado o admin
        if user.rol == "tecnico" and facility.tecnico.id != user.id:
            return Response(
                {"detail": "No eres el técnico asignado"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            start_facility(
                facility=facility,
                responsable=user
            )
        except FacilityActionError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Instalación iniciada correctamente"},
            status=status.HTTP_200_OK
        )
