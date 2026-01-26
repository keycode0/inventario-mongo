from rest_framework import serializers
from bson import ObjectId

from config.apps.inventory.models.movement import Movement


class MovementSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    item = serializers.SerializerMethodField()
    responsable = serializers.SerializerMethodField()

    tipo_movimiento = serializers.CharField()
    origen = serializers.SerializerMethodField()
    destino = serializers.SerializerMethodField()
    fecha = serializers.DateTimeField()

    # =========================
    # SERIALIZERS CUSTOM
    # =========================
    def get_item(self, obj):
        return {
            "id": str(obj.item.id),
            "codigo": obj.item.codigo,
            "nombre": obj.item.nombre,
        }

    def get_responsable(self, obj):
        return {
            "id": str(obj.responsable.id),
            "username": obj.responsable.username,
            "rol": obj.responsable.rol,
        }

    def _serialize_location(self, location: dict):
        return {
            "tipo": location.get("tipo"),
            "id": str(location.get("id")) if isinstance(location.get("id"), ObjectId) else location.get("id"),
        }

    def get_origen(self, obj):
        return self._serialize_location(obj.origen)

    def get_destino(self, obj):
        return self._serialize_location(obj.destino)
