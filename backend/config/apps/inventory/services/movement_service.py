from datetime import datetime, timezone

from config.apps.inventory.models.movement import Movement
from config.apps.inventory.models.item import Item
from config.apps.users.models.user import User


def register_movement(
    *,
    item: Item,
    tipo_movimiento: str,
    origen: dict,
    destino: dict,
    responsable: User,
):
    """
    Registra un movimiento y actualiza la ubicación del item.
    """

    movement = Movement.objects.create(
        item=item,
        tipo_movimiento=tipo_movimiento,
        origen=origen,
        destino=destino,
        responsable=responsable,
        fecha=datetime.now(timezone.utc),
    )

    # 🔁 Actualizar ubicación actual del item
    item.ubicacion_actual_id = destino.get("id")
    item.save()

    return movement
