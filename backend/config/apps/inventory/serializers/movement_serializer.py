from rest_framework import serializers
from config.apps.inventory.models.movement import Movement
from config.apps.inventory.models.item import Item
from config.apps.users.models.user import User


class MovementSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    item_id = serializers.CharField(write_only=True)
    responsable_id = serializers.CharField(write_only=True)

    tipo_movimiento = serializers.CharField()
    origen = serializers.DictField()
    destino = serializers.DictField()
    fecha = serializers.DateTimeField(required=False)

    def validate_item_id(self, value):
        item = Item.objects(id=value, is_active=True).first()
        if not item:
            raise serializers.ValidationError(
                "El item no existe o está inactivo"
            )
        return item

    def validate_responsable_id(self, value):
        user = User.objects(id=value, is_active=True).first()
        if not user:
            raise serializers.ValidationError(
                "El responsable no existe o está inactivo"
            )
        return user

    def create(self, validated_data):
        item = validated_data.pop("item_id")
        responsable = validated_data.pop("responsable_id")

        return Movement.objects.create(
            item=item,
            responsable=responsable,
            **validated_data
        )
