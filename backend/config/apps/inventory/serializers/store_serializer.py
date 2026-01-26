from rest_framework import serializers
from config.apps.inventory.models.store import Store


class StoreSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre_bodega = serializers.CharField()
    ubicacion = serializers.DictField()

    def to_representation(self, instance):
        return {
            "id": str(instance.id),
            "nombre_bodega": instance.nombre_bodega,
            "ubicacion": instance.ubicacion,
        }

    def create(self, validated_data):
        store = Store(**validated_data)
        store.save()
        return store

    def update(self, instance, validated_data):
        instance.nombre_bodega = validated_data.get(
            "nombre_bodega", instance.nombre_bodega
        )
        instance.ubicacion = validated_data.get(
            "ubicacion", instance.ubicacion
        )
        instance.save()
        return instance
