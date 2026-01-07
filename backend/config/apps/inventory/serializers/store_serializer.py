from rest_framework import serializers
from config.apps.inventory.models.store import Store


class StoreSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    nombre_bodega = serializers.CharField()
    ubicacion = serializers.DictField()

    def create(self, validated_data):
        return Store.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre_bodega = validated_data.get(
            "nombre_bodega", instance.nombre_bodega
        )
        instance.ubicacion = validated_data.get(
            "ubicacion", instance.ubicacion
        )
        instance.save()
        return instance
