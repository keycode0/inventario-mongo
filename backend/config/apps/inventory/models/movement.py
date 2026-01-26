import mongoengine as me
from datetime import datetime, timezone

from config.apps.base.base_document import BaseDocument
from config.apps.inventory.models.item import Item
from config.apps.users.models.user import User


class Movement(BaseDocument):
    """
    Movimiento de inventario (auditoría).
    Cada documento representa un evento real e inmutable.
    """

    item = me.ReferenceField(
        Item,
        required=True,
        reverse_delete_rule=me.DENY
    )

    tipo_movimiento = me.StringField(required=True)

    origen = me.DictField(required=True)
    destino = me.DictField(required=True)

    fecha = me.DateTimeField(
        default=lambda: datetime.now(timezone.utc)
    )

    responsable = me.ReferenceField(
        User,
        required=True
    )

    meta = {
        "collection": "movimientos",
        "indexes": [
            "tipo_movimiento",
            "fecha",
        ],
    }
