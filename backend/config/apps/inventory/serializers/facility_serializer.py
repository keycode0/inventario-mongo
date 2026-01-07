from rest_framework import serializers
from config.apps.inventory.models.facility import Facility
from config.apps.inventory.models.customer import Customer
from config.apps.users.models.user import User


class FacilitySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    codigo_instalacion = serializers.CharField()

    cliente_id = serializers.CharField(write_only=True)
    tecnico_id = serializers.CharField(write_only=True)

    direccion_instalacion = serializers.CharField(required=False, allow_blank=True)

    estado = serializers.ChoiceField(
        choices=["planificada", "en_proceso", "finalizada", "cancelada"],
        default="planificada"
    )

    fecha_programada = serializers.DateTimeField(required=False)
    fecha_inicio = serializers.DateTimeField(required=False)
    fecha_fin = serializers.DateTimeField(required=False)

    items_planificados = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    def validate_cliente_id(self, value):
        cliente = Customer.objects(id=value, is_active=True).first()
        if not cliente:
            raise serializers.ValidationError(
                "Cliente no existe o está inactivo"
            )
        return cliente

    def validate_tecnico_id(self, value):
        tecnico = User.objects(id=value, is_active=True).first()
        if not tecnico:
            raise serializers.ValidationError(
                "Técnico no existe o está inactivo"
            )
        return tecnico

    def create(self, validated_data):
        cliente = validated_data.pop("cliente_id")
        tecnico = validated_data.pop("tecnico_id")

        return Facility.objects.create(
            cliente=cliente,
            tecnico=tecnico,
            **validated_data
        )

    def update(self, instance, validated_data):
        if "cliente_id" in validated_data:
            instance.cliente = validated_data.pop("cliente_id")

        if "tecnico_id" in validated_data:
            instance.tecnico = validated_data.pop("tecnico_id")

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance
