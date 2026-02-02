from bson import ObjectId
from rest_framework import serializers

from config.apps.inventory.models.facility import Facility
from config.apps.inventory.models.customer import Customer
from config.apps.inventory.models.item import Item
from config.apps.users.models.user import User


# ======================================================
# SERIALIZER: ITEM DENTRO DE INSTALACIÓN
# ======================================================
class FacilityItemSerializer(serializers.Serializer):
    """
    Item planificado dentro de una instalación
    """

    item_id = serializers.CharField()
    origen_bodega_id = serializers.CharField()

    accion_final = serializers.ChoiceField(
        choices=["queda_cliente", "retorna_bodega"],
        required=False,
        allow_null=True
    )

    bodega_retorno_id = serializers.CharField(
        required=False,
        allow_null=True
    )

    # -------------------------
    # VALIDACIONES DE IDS
    # -------------------------
    def validate_item_id(self, value):
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("item_id inválido")

        item = Item.objects(id=value, is_active=True).first()
        if not item:
            raise serializers.ValidationError(
                "El item no existe o está inactivo"
            )

        return value

    def validate_origen_bodega_id(self, value):
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("origen_bodega_id inválido")
        return value

    # -------------------------
    # VALIDACIÓN DE NEGOCIO
    # -------------------------
    def validate(self, data):
        item_id = data.get("item_id")
        origen_bodega_id = data.get("origen_bodega_id")

        item = Item.objects(id=item_id).first()
        if not item:
            raise serializers.ValidationError(
                "El item no existe"
            )

        if not item.ubicacion_actual_id:
            raise serializers.ValidationError(
                "El item no tiene una ubicación actual definida"
            )

        if str(item.ubicacion_actual_id) != origen_bodega_id:
            raise serializers.ValidationError(
                "El item no se encuentra en la bodega indicada"
            )

        # -------------------------
        # VALIDACIÓN CONTEXTUAL (FINALIZACIÓN)
        # -------------------------
        accion = data.get("accion_final")
        is_finishing = self.context.get("is_finishing", False)

        # 🔹 Antes de finalizar → no exigir acción final
        if not is_finishing:
            return data

        # 🔹 Al finalizar → accion_final es obligatoria
        if not accion:
            raise serializers.ValidationError(
                "accion_final es obligatoria al finalizar la instalación"
            )

        if accion == "retorna_bodega":
            bodega_id = data.get("bodega_retorno_id")

            if not bodega_id:
                raise serializers.ValidationError(
                    "bodega_retorno_id es obligatorio cuando retorna a bodega"
                )

            if not ObjectId.is_valid(bodega_id):
                raise serializers.ValidationError(
                    "bodega_retorno_id inválido"
                )

        if accion == "queda_cliente" and data.get("bodega_retorno_id"):
            raise serializers.ValidationError(
                "bodega_retorno_id no debe existir cuando queda en cliente"
            )

        return data


# ======================================================
# SERIALIZER: INSTALACIÓN
# ======================================================
class FacilitySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    codigo_instalacion = serializers.CharField()

    cliente_id = serializers.CharField(write_only=True)
    tecnico_id = serializers.CharField(write_only=True)

    direccion_instalacion = serializers.CharField(
        required=False,
        allow_blank=True
    )

    estado = serializers.ChoiceField(
        choices=["planificada", "en_proceso", "finalizada", "cancelada"],
        read_only=True
    )

    fecha_programada = serializers.DateTimeField(required=False)
    fecha_inicio = serializers.DateTimeField(read_only=True)
    fecha_fin = serializers.DateTimeField(read_only=True)

    items_planificados = FacilityItemSerializer(
        many=True,
        required=False
    )

    # -------------------------
    # VALIDACIONES DE RELACIONES
    # -------------------------
    def validate_cliente_id(self, value):
        cliente = Customer.objects(id=value, is_active=True).first()
        if not cliente:
            raise serializers.ValidationError(
                "Cliente no existe o está inactivo"
            )
        return cliente

    def validate_tecnico_id(self, value):
        tecnico = User.objects(
            id=value,
            is_active=True,
            rol="tecnico"
        ).first()
        if not tecnico:
            raise serializers.ValidationError(
                "Técnico no existe o está inactivo"
            )
        return tecnico

    # -------------------------
    # VALIDACIÓN GLOBAL
    # -------------------------
    def validate(self, data):
        items = data.get("items_planificados")

        if not items:
            return data

        seen_items = set()
        estado_actual = (
            self.instance.estado if self.instance else "planificada"
        )

        for item in items:
            item_id = item["item_id"]

            if item_id in seen_items:
                raise serializers.ValidationError(
                    f"Item {item_id} está duplicado"
                )
            seen_items.add(item_id)

            # 🔒 Solo permitir accion_final al finalizar
            if estado_actual != "en_proceso":
                if item.get("accion_final"):
                    raise serializers.ValidationError(
                        "accion_final solo puede definirse al finalizar la instalación"
                    )

        return data

    # -------------------------
    # CREATE
    # -------------------------
    def create(self, validated_data):
        cliente = validated_data.pop("cliente_id")
        tecnico = validated_data.pop("tecnico_id")
        items = validated_data.pop("items_planificados", [])

        return Facility.objects.create(
            cliente=cliente,
            tecnico=tecnico,
            items_planificados=items,
            **validated_data
        )

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, instance, validated_data):
        validated_data.pop("cliente_id", None)
        validated_data.pop("tecnico_id", None)

        if (
            "items_planificados" in validated_data
            and instance.estado != "planificada"
        ):
            raise serializers.ValidationError(
                "No se pueden modificar items en una instalación en proceso o finalizada"
            )

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance
