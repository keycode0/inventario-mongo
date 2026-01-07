import mongoengine as me
from datetime import datetime, timezone

from config.apps.base.base_document import BaseDocument
from config.apps.inventory.models.customer import Customer
from config.apps.users.models.user import User


class Facility(BaseDocument):
    """
    Representa una instalación (facility) realizada para un cliente.
    """

    codigo_instalacion = me.StringField(required=True, unique=True)

    cliente = me.ReferenceField(
        Customer,
        required=True,
        reverse_delete_rule=me.DENY
    )

    tecnico = me.ReferenceField(
        User,
        required=True
    )

    direccion_instalacion = me.StringField()

    estado = me.StringField(
        choices=[
            "planificada",
            "en_proceso",
            "finalizada",
            "cancelada"
        ],
        default="planificada"
    )

    fecha_programada = me.DateTimeField()
    fecha_inicio = me.DateTimeField()
    fecha_fin = me.DateTimeField()

    items_planificados = me.ListField(me.DictField())

    meta = {
        "collection": "instalaciones",  # NO se cambia para no romper datos
        "indexes": ["codigo_instalacion", "estado"],
    }
