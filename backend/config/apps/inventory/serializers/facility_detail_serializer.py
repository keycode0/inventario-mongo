from rest_framework import serializers
from config.apps.inventory.models import Item, Store


class FacilityDetailSerializer(serializers.Serializer):
    id = serializers.CharField()
    codigo_instalacion = serializers.CharField()
    estado = serializers.CharField()

    fecha_programada = serializers.DateTimeField(allow_null=True)
    fecha_inicio = serializers.DateTimeField(allow_null=True)
    fecha_fin = serializers.DateTimeField(allow_null=True)

    cliente = serializers.SerializerMethodField()
    tecnico = serializers.SerializerMethodField()
    items_planificados = serializers.SerializerMethodField()

    # =========================
    # CLIENTE
    # =========================
    def get_cliente(self, obj):
        if not obj.cliente:
            return None

        return {
            "id": str(obj.cliente.id),
            "nombre_cliente": obj.cliente.nombre_cliente,
        }

    # =========================
    # TÉCNICO
    # =========================
    def get_tecnico(self, obj):
        if not obj.tecnico:
            return None

        return {
            "id": str(obj.tecnico.id),
            "username": obj.tecnico.username,
        }

    # =========================
    # ITEMS PLANIFICADOS
    # =========================
    def get_items_planificados(self, obj):
        result = []

        for it in obj.items_planificados:
            item_id = it.get("item_id")
            store_id = it.get("origen_bodega_id")  # legacy field

            item = Item.objects(id=item_id).first() if item_id else None
            store = Store.objects(id=store_id).first() if store_id else None

            result.append({
                "item": {
                    "id": str(item.id) if item else None,
                    "nombre": item.nombre if item else None,
                    "codigo": item.codigo if item else None,
                },
                "origen_store": {
                    "id": str(store.id) if store else None,
                    "nombre_bodega": store.nombre_bodega if store else None,
                },
                "accion_final": it.get("accion_final"),
                "bodega_retorno_id": it.get("bodega_retorno_id"),
            })

        return result
