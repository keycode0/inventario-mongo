from config.apps.inventory.models.item import Item


ALLOWED_ITEM_STATES = ["operativo", "dañado", "baja"]


def soft_delete_item(item: Item) -> None:
    """
    Desactiva lógicamente un item.
    """
    item.is_active = False
    item.save()


def change_item_status(item: Item, new_status: str) -> None:
    """
    Cambia el estado del item validando valores permitidos.
    """
    if new_status not in ALLOWED_ITEM_STATES:
        raise ValueError(f"Estado no válido: {new_status}")

    item.estado = new_status
    item.save()


def update_item_location(item: Item, location_id) -> None:
    """
    Actualiza la ubicación actual del item.
    """
    item.ubicacion_actual_id = location_id
    item.save()
