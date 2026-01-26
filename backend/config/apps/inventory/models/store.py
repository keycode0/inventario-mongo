import mongoengine as me
from config.apps.base.base_document import BaseDocument


class Store(BaseDocument):
    nombre_bodega = me.StringField(required=True)
    ubicacion = me.DictField()
    activo = me.BooleanField(default=True)

    meta = {
        "collection": "bodegas",
    }