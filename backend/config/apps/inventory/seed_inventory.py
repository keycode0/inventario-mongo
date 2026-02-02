import os
import django
from datetime import datetime, timezone

# ======================================================
# BOOTSTRAP DJANGO
# ======================================================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# ======================================================
# IMPORTS MODELOS
# ======================================================
from config.apps.inventory.models.category import Category
from config.apps.inventory.models.subcategory import SubCategory
from config.apps.inventory.models.store import Store
from config.apps.inventory.models.supplier import Supplier
from config.apps.inventory.models.customer import Customer
from config.apps.inventory.models.item import Item
from config.apps.inventory.models.movement import Movement
from config.apps.inventory.models.facility import Facility
from config.apps.inventory.models.vehicle import Vehicle

from config.apps.users.models.user import User
from config.apps.users.permissions.roles import Roles


# ======================================================
# HELPER SEGURO (BaseDocument compatible)
# ======================================================
def get_or_create(model, defaults=None, **query):
    """
    get_or_create seguro para MongoEngine + BaseDocument
    - Filtra is_active=True
    - Ignora campos inexistentes
    """
    obj = model.objects(is_active=True, **query).first()
    if obj:
        return obj, False

    data = {}
    data.update(query)
    if defaults:
        data.update(defaults)

    allowed_fields = set(model._fields.keys())
    clean_data = {k: v for k, v in data.items() if k in allowed_fields}

    obj = model(**clean_data)
    obj.save()
    return obj, True


# ======================================================
# SEEDERS
# ======================================================
def seed_users():
    print("🔐 Creando usuarios...")

    admin, _ = get_or_create(
        User,
        username="admin",
        defaults={"rol": Roles.ADMIN.value}
    )
    if not admin.password_hash:
        admin.set_password("admin123")
        admin.save()

    tecnico, _ = get_or_create(
        User,
        username="tecnico1",
        defaults={"rol": Roles.TECNICO.value}
    )
    if not tecnico.password_hash:
        tecnico.set_password("tecnico123")
        tecnico.save()

    return admin, tecnico


def seed_categories():
    print("📦 Creando categorías...")

    redes, _ = get_or_create(Category, nombre_categoria="Redes")
    computo, _ = get_or_create(Category, nombre_categoria="Computación")

    return redes, computo


def seed_subcategories(redes, computo):
    print("📁 Creando subcategorías...")

    router, _ = get_or_create(
        SubCategory,
        categoria=redes,
        nombre="Routers"
    )
    switch, _ = get_or_create(
        SubCategory,
        categoria=redes,
        nombre="Switches"
    )
    laptop, _ = get_or_create(
        SubCategory,
        categoria=computo,
        nombre="Laptops"
    )

    return router, switch, laptop


def seed_stores():
    print("🏬 Creando bodegas...")

    store, _ = get_or_create(
        Store,
        nombre_bodega="Bodega Central",
        defaults={
            "ubicacion": {"ciudad": "Quito"},
            "activo": True  # Store sí tiene este campo
        }
    )

    return store


def seed_suppliers():
    print("🚚 Creando proveedores...")

    supplier, _ = get_or_create(
        Supplier,
        nombre_proveedor="Proveedor Tech",
        defaults={"sucursal": "Matriz"}
    )

    return supplier


def seed_customers():
    print("👥 Creando clientes...")

    customer, _ = get_or_create(
        Customer,
        nombre_cliente="Empresa XYZ",
        defaults={
            "sucursal": "Quito",
            "ubicacion": {"direccion": "Av. Amazonas"}
        }
    )

    return customer


def seed_vehicles():
    print("🚗 Creando vehículos...")

    vehicle, _ = get_or_create(
        Vehicle,
        placa="ABC-123",
        defaults={
            "modelo": "Toyota Hilux",
            "anio": 2022
        }
    )

    return vehicle


def seed_items(subcategory):
    print("🧾 Creando ítems...")

    item, _ = get_or_create(
        Item,
        codigo="ITM-001",
        defaults={
            "nombre": "Router Mikrotik",
            "subcategoria": subcategory,
            "marca": "Mikrotik",
            "modelo": "RB4011",
            "estado": "operativo"
        }
    )

    return item


def seed_movements(item, user):
    print("🔄 Creando movimientos...")

    exists = Movement.objects(
        item=item,
        tipo_movimiento="ingreso"
    ).first()

    if not exists:
        Movement(
            item=item,
            tipo_movimiento="ingreso",
            origen={"tipo": "proveedor"},
            destino={"tipo": "bodega"},
            responsable=user
        ).save()


def seed_facility(customer, tecnico, item):
    print("🏗️ Creando instalación...")

    exists = Facility.objects(
        codigo_instalacion="FAC-001"
    ).first()

    if not exists:
        Facility(
            codigo_instalacion="FAC-001",
            cliente=customer,
            tecnico=tecnico,
            direccion_instalacion="Av. Principal 123",
            estado="planificada",
            fecha_programada=datetime.now(timezone.utc),
            items_planificados=[
                {
                    "item_id": str(item.id),
                    "descripcion": item.nombre
                }
            ]
        ).save()


# ======================================================
# MAIN
# ======================================================
def run():
    print("\n🚀 INICIANDO SEED DE INVENTARIO\n")

    admin, tecnico = seed_users()
    redes, computo = seed_categories()
    router, _, _ = seed_subcategories(redes, computo)
    seed_stores(Sertecpet)
    seed_suppliers()
    customer = seed_customers()
    seed_vehicles()
    item = seed_items(router)
    seed_movements(item, admin)
    seed_facility(customer, tecnico, item)

    print("\n✅ SEED COMPLETADO CON ÉXITO\n")


if __name__ == "__main__":
    run()
