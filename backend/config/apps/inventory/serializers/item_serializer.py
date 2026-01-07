from rest_framework import serializers
from config.apps.inventory.models.item import Item
from config.apps.inventory.models.subcategory import SubCategory


class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    codigo = serializers.CharField()
    nombre = serializers.CharField()

    subcategoria_id = serializers.CharField(write_only=True)

    marca = serializers.CharField(required=False, allow_blank=True)
    modelo = serializers.CharField(required=False, allow_blank=True)
    serial = serializers.CharField(required=False, allow_blank=True)

    estado = serializers.ChoiceField(
        choices=["operativo", "dañado", "obsoleto", "baja"],
        default="operativo"
    )

    ubicacion_actual_id = serializers.CharField(
        required=False, allow_null=True
    )

    def validate_subcategoria_id(self, value):
        subcategoria = SubCategory.objects(id=value, is_active=True).first()
        if not subcategoria:
            raise serializers.ValidationError(
                "La subcategoría no existe o está inactiva"
            )
        return subcategoria

    def create(self, validated_data):
        subcategoria = validated_data.pop("subcategoria_id")
        return Item.objects.create(
            subcategoria=subcategoria,
            **validated_data
        )

    def update(self, instance, validated_data):
        if "subcategoria_id" in validated_data:
            instance.subcategoria = validated_data.pop("subcategoria_id")

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance
