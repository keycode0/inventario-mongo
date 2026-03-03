from datetime import datetime, timezone

from config.apps.inventory.models.movement import Movement
from config.apps.inventory.models.item import Item
from config.apps.users.models.user import User


from enum import Enum

class MovementType(str, Enum):
    INGRESO_COMPRA = "INGRESO_COMPRA"
    SALIDA_INSTALACION = "SALIDA_INSTALACION"
    INSTALADO_CLIENTE = "INSTALADO_CLIENTE"
    RETORNO_INSTALACION = "RETORNO_INSTALACION"
    TRASLADO_BODEGA = "TRASLADO_BODEGA"
    ENVIO_REPARACION = "ENVIO_REPARACION"
    BAJA = "BAJA"

ALLOWED_MOVEMENT_TYPES = [m.value for m in list(MovementType)]


class MovementServiceError(ValueError):
    pass


from dataclasses import dataclass
from typing import Any

@dataclass
class LocationData:
    tipo: str
    id: Any

def _validate_endpoint(data: dict, name: str) -> LocationData:
    if not isinstance(data, dict):
        raise MovementServiceError(f"{name} debe ser un diccionario")

    if "tipo" not in data or "id" not in data:
        raise MovementServiceError(
            f"{name} debe contener 'tipo' e 'id'"
        )
    return LocationData(tipo=data["tipo"], id=data["id"])


def register_movement(
    *,
    item: Item,
    tipo_movimiento: str,
    origen: dict,
    destino: dict,
    responsable: User,
) -> Movement:
    """
    Registra un movimiento y actualiza la ubicación actual del item.
    """

    # =========================
    # VALIDACIONES
    # =========================
    if tipo_movimiento not in ALLOWED_MOVEMENT_TYPES:
        raise MovementServiceError(
            f"Tipo de movimiento no permitido: {tipo_movimiento}"
        )

    if not item.is_active:
        raise MovementServiceError("Item inactivo")

    _validate_endpoint(origen, "origen")
    _validate_endpoint(destino, "destino")

    # =========================
    # CREAR MOVIMIENTO
    # =========================
    movement = Movement.objects.create(
        item=item,
        tipo_movimiento=tipo_movimiento,
        origen=origen,
        destino=destino,
        responsable=responsable,
        fecha=datetime.now(timezone.utc),
    )

    # =========================
    # ACTUALIZAR UBICACIÓN DEL ITEM
    # =========================
    item.ubicacion_actual_id = destino["id"]
    item.save()

    return movement

