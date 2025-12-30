import mongoengine as me
from .base import BaseDocument


class User(BaseDocument):
    """
    Colección: usuarios
    Maneja los usuarios del sistema y sus roles.
    """

    user_id = me.IntField(required=True, unique=True)
    username = me.StringField(required=True, unique=True)
    rol = me.StringField(
        required=True,
        choices=["admin", "tecnico", "operador"]
    )

    meta = {
        "collection": "usuarios",
        "indexes": ["user_id", "username"]
    }
