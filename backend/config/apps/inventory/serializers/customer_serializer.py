from rest_framework import serializers
from config.apps.inventory.models.customer import Customer


class CustomerSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    nombre_cliente = serializers.CharField()
    sucursal = serializers.CharField(required=False, allow_blank=True)
    ubicacion = serializers.DictField()

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
