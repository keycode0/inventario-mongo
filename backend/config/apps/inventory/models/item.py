import mongoengine as me
from config.apps.base.base_document import BaseDocument
from config.apps.inventory.models.subcategory import SubCategory


class Item(BaseDocument):
    codigo = me.StringField(required=True, unique=True)
    nombre = me.StringField(required=True)

    subcategoria = me.ReferenceField(
        SubCategory,
        required=True,
        reverse_delete_rule=me.DENY
    )

    marca = me.StringField()
    modelo = me.StringField()
    serial = me.StringField()

    estado = me.StringField(
        choices=["operativo", "dañado", "obsoleto", "baja"],
        default="operativo"
    )

    ubicacion_actual_id = me.ObjectIdField(required=True)

    meta = {
        "collection": "items",
        "indexes": ["codigo", "estado"],
    }
