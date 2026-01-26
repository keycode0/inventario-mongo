from config.apps.inventory.models.facility import Facility
from config.apps.inventory.models.item import Item
from config.apps.users.models.user import User

from config.apps.inventory.services.facility_service import change_facility_status
from config.apps.inventory.services.movement_service import register_movement


class FacilityActionError(ValueError):
    pass


# =========================
# INICIAR INSTALACIÓN
# =========================
def start_facility(*, facility: Facility, responsable: User) -> None:
    if not facility.is_active:
        raise FacilityActionError("La instalación está inactiva")

    if facility.estado != "planificada":
        raise FacilityActionError(
            "Solo se puede iniciar una instalación planificada"
        )

    if not facility.items_planificados:
        raise FacilityActionError(
            "La instalación no tiene items planificados"
        )

    for data in facility.items_planificados:
        item_id = data.get("item_id")
        origen_bodega_id = data.get("origen_bodega_id")

        if not item_id or not origen_bodega_id:
            raise FacilityActionError(
                "Cada item debe tener item_id y origen_bodega_id"
            )

        item = Item.objects(id=item_id, is_active=True).first()
        if not item:
            raise FacilityActionError("Item no encontrado")

        if item.estado != "operativo":
            raise FacilityActionError(
                f"Item {item.codigo} no está operativo"
            )

    # Cambiar estado
    change_facility_status(facility, "en_proceso")

    # Registrar salida a instalación (por item)
    for data in facility.items_planificados:
        item = Item.objects.get(id=data["item_id"])

        register_movement(
            item=item,
            tipo_movimiento="SALIDA_INSTALACION",
            origen={
                "tipo": "bodega",
                "id": data["origen_bodega_id"],
            },
            destino={
                "tipo": "instalacion",
                "id": facility.id,
            },
            responsable=responsable,
        )


# =========================
# FINALIZAR INSTALACIÓN
# =========================
def finish_facility(*, facility: Facility, responsable: User) -> None:
    if not facility.is_active:
        raise FacilityActionError("La instalación está inactiva")

    if facility.estado != "en_proceso":
        raise FacilityActionError(
            "Solo se puede finalizar una instalación en proceso"
        )

    for data in facility.items_planificados:
        item = Item.objects(id=data.get("item_id"), is_active=True).first()
        accion = data.get("accion_final")

        if not item:
            raise FacilityActionError("Item no encontrado")

        if accion == "queda_cliente":
            register_movement(
                item=item,
                tipo_movimiento="INSTALADO_CLIENTE",
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
            bodega_id = data.get("bodega_retorno_id")
            if not bodega_id:
                raise FacilityActionError(
                    f"Item {item.codigo} debe indicar bodega de retorno"
                )

            register_movement(
                item=item,
                tipo_movimiento="RETORNO_INSTALACION",
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
            raise FacilityActionError(
                f"Acción final no válida para item {item.codigo}"
            )

    change_facility_status(facility, "finalizada")
