from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.facility import Facility
from config.apps.inventory.services.facility_service import FacilityService, FacilityServiceError
from config.apps.users.permissions.facility_permissions import FacilityPermission


class FacilityFinishView(APIView):
    permission_classes = [FacilityPermission]

    def post(self, request, pk):
        facility = Facility.objects(id=pk, is_active=True).first()
        if not facility:
            return Response(
                {"detail": "Instalación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        items_data = request.data.get("items_planificados")
        if not items_data:
            return Response(
                {"detail": "Debe enviar items_planificados"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔁 Actualizar SOLO accion_final y bodega_retorno_id
        items_map = {i["item_id"]: i for i in items_data}

        for item in facility.items_planificados:
            data = items_map.get(item["item_id"])
            if not data:
                return Response(
                    {"detail": f"Falta acción final para item {item['item_id']}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            item["accion_final"] = data.get("accion_final")
            item["bodega_retorno_id"] = data.get("bodega_retorno_id")

        try:
            FacilityService.finish_facility(
                facility=facility,
                responsable=request.user
            )
        except FacilityServiceError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Instalación finalizada correctamente"},
            status=status.HTTP_200_OK
        )
