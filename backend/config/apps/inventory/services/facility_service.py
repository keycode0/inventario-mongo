from mongoengine.connection import get_connection

from config.apps.inventory.models.facility import Facility
from config.apps.inventory.models.item import Item
from config.apps.users.models.user import User

from config.apps.inventory.services.movement_service import register_movement, MovementType

ALLOWED_FACILITY_STATES = [
    "planificada",
    "en_proceso",
    "finalizada",
    "cancelada",
]

class FacilityServiceError(ValueError):
    pass

class FacilityService:
    @staticmethod
    def soft_delete_facility(facility: Facility) -> None:
        """
        Desactiva lógicamente una instalación.
        """
        facility.is_active = False
        facility.save()

    @staticmethod
    def change_facility_status(facility: Facility, new_status: str) -> None:
        """
        Cambia el estado de la instalación validando la transición.
        """
        if new_status not in ALLOWED_FACILITY_STATES:
            raise FacilityServiceError(f"Estado no permitido: {new_status}")

        facility.estado = new_status
        facility.save()

    @staticmethod
    def start_facility(*, facility: Facility, responsable: User) -> None:
        if not facility.is_active:
            raise FacilityServiceError("La instalación está inactiva")

        if facility.estado != "planificada":
            raise FacilityServiceError("Solo se puede iniciar una instalación planificada")

        if not facility.items_planificados:
            raise FacilityServiceError("La instalación no tiene items planificados")

        # Preparar datos y validar ítems
        items_to_process = []
        for data in facility.items_planificados:
            item_id = data.get("item_id")
            origen_bodega_id = data.get("origen_bodega_id")

            if not item_id or not origen_bodega_id:
                raise FacilityServiceError("Cada item debe tener item_id y origen_bodega_id")

            item = Item.objects(id=item_id, is_active=True).first()
            if not item:
                raise FacilityServiceError("Item no encontrado")

            if item.estado != "operativo":
                raise FacilityServiceError(f"Item {item.codigo} no está operativo")

            items_to_process.append({
                "item": item,
                "origen_id": origen_bodega_id
            })

        # Utilizar transacción de MongoDB
        connection = get_connection()
        with connection.start_session() as session:
            with session.start_transaction():
                FacilityService.change_facility_status(facility, "en_proceso")

                for process_data in items_to_process:
                    register_movement(
                        item=process_data["item"],
                        tipo_movimiento=MovementType.SALIDA_INSTALACION.value,
                        origen={
                            "tipo": "bodega",
                            "id": process_data["origen_id"],
                        },
                        destino={
                            "tipo": "instalacion",
                            "id": facility.id,
                        },
                        responsable=responsable,
                    )

    @staticmethod
    def finish_facility(*, facility: Facility, responsable: User) -> None:
        if not facility.is_active:
            raise FacilityServiceError("La instalación está inactiva")

        if facility.estado != "en_proceso":
            raise FacilityServiceError("Solo se puede finalizar una instalación en proceso")

        items_to_process = []
        for data in facility.items_planificados:
            item = Item.objects(id=data.get("item_id"), is_active=True).first()
            accion = data.get("accion_final")

            if not item:
                raise FacilityServiceError("Item no encontrado")
                
            items_to_process.append({
                "item": item,
                "accion": accion,
                "bodega_retorno_id": data.get("bodega_retorno_id")
            })

        # Utilizar transacción de MongoDB
        connection = get_connection()
        with connection.start_session() as session:
            with session.start_transaction():
                FacilityService.change_facility_status(facility, "finalizada")

                for process_data in items_to_process:
                    item = process_data["item"]
                    accion = process_data["accion"]

                    if accion == "queda_cliente":
                        register_movement(
                            item=item,
                            tipo_movimiento=MovementType.INSTALADO_CLIENTE.value,
                            origen={
                                "tipo": "instalacion",
                                "id": facility.id,
                            },
                            destino={
                                "tipo": "cliente",
                                "id": facility.cliente.id,
                            },
                            responsable=responsable,
                        )
                    elif accion == "retorna_bodega":
                        bodega_id = process_data["bodega_retorno_id"]
                        if not bodega_id:
                            raise FacilityServiceError(f"Item {item.codigo} debe indicar bodega de retorno")

                        register_movement(
                            item=item,
                            tipo_movimiento=MovementType.RETORNO_INSTALACION.value,
                            origen={
                                "tipo": "instalacion",
                                "id": facility.id,
                            },
                            destino={
                                "tipo": "bodega",
                                "id": bodega_id,
                            },
                            responsable=responsable,
                        )
                    else:
                        raise FacilityServiceError(f"Acción final no válida para item {item.codigo}")
