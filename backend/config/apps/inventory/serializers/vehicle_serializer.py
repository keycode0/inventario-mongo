from rest_framework import serializers
from config.apps.inventory.models.vehicle import Vehicle


class VehicleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    placa = serializers.CharField()
    modelo = serializers.CharField(required=False, allow_blank=True)
    anio = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
