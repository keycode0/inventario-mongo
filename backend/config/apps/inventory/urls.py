from django.urls import path

# =========================
# CATEGORY
# =========================
from config.apps.inventory.views.category_views import (
    CategoryListCreateView,
    CategoryDetailView,
)

# =========================
# SUBCATEGORY
# =========================
from config.apps.inventory.views.subcategory_views import (
    SubCategoryListCreateView,
    SubCategoryDetailView,
)

# =========================
# ITEMS
# =========================
from config.apps.inventory.views.item_views import (
    ItemListCreateView,
    ItemDetailView,
)

# =========================
# STORE (BODEGAS)
# =========================
from config.apps.inventory.views.store_views import (
    StoreListCreateView,
    StoreDetailView,
)

# =========================
# CUSTOMER (CLIENTES)
# =========================
from config.apps.inventory.views.customer_views import (
    CustomerListCreateView,
    CustomerDetailView,
)

# =========================
# SUPPLIER (PROVEEDORES)
# =========================
from config.apps.inventory.views.supplier_views import (
    SupplierListCreateView,
    SupplierDetailView,
)

# =========================
# VEHICLE (VEHÍCULOS)
# =========================
from config.apps.inventory.views.vehicle_views import (
    VehicleListCreateView,
    VehicleDetailView,
)

# =========================
# FACILITY (INSTALACIONES)
# =========================
from config.apps.inventory.views.facility_views import (
    FacilityListCreateView,
    FacilityDetailView,
)

# =========================
# FACILITY ACTIONS (ORQUESTACIÓN)
# =========================
from config.apps.inventory.views.facility_start_view import FacilityStartView
from config.apps.inventory.views.facility_finish_view import FacilityFinishView

# =========================
# MOVEMENTS (AUDITORÍA - SOLO LECTURA)
# =========================
from config.apps.inventory.views.movement_views import (
    MovementListView,
)


urlpatterns = [
    # =========================
    # CATEGORY
    # =========================
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<str:pk>/", CategoryDetailView.as_view(), name="category-detail"),

    # =========================
    # SUBCATEGORY
    # =========================
    path("subcategories/", SubCategoryListCreateView.as_view(), name="subcategory-list-create"),
    path("subcategories/<str:pk>/", SubCategoryDetailView.as_view(), name="subcategory-detail"),

    # =========================
    # ITEMS
    # =========================
    path("items/", ItemListCreateView.as_view(), name="item-list-create"),
    path("items/<str:pk>/", ItemDetailView.as_view(), name="item-detail"),

    # =========================
    # STORES (BODEGAS)
    # =========================
    path("stores/", StoreListCreateView.as_view(), name="store-list-create"),
    path("stores/<str:pk>/", StoreDetailView.as_view(), name="store-detail"),

    # =========================
    # CUSTOMERS
    # =========================
    path("customers/", CustomerListCreateView.as_view(), name="customer-list-create"),
    path("customers/<str:pk>/", CustomerDetailView.as_view(), name="customer-detail"),

    # =========================
    # SUPPLIERS
    # =========================
    path("suppliers/", SupplierListCreateView.as_view(), name="supplier-list-create"),
    path("suppliers/<str:pk>/", SupplierDetailView.as_view(), name="supplier-detail"),

    # =========================
    # VEHICLES
    # =========================
    path("vehicles/", VehicleListCreateView.as_view(), name="vehicle-list-create"),
    path("vehicles/<str:pk>/", VehicleDetailView.as_view(), name="vehicle-detail"),

    # =========================
    # FACILITIES (CRUD CONTROLADO)
    # =========================
    path("facilities/", FacilityListCreateView.as_view(), name="facility-list-create"),
    path("facilities/<str:pk>/", FacilityDetailView.as_view(), name="facility-detail"),

    # =========================
    # FACILITY ACTIONS (FLUJO DE NEGOCIO)
    # =========================
    path(
        "facilities/<str:pk>/start/",
        FacilityStartView.as_view(),
        name="facility-start",
    ),
    path(
        "facilities/<str:pk>/finish/",
        FacilityFinishView.as_view(),
        name="facility-finish",
    ),

    # =========================
    # MOVEMENTS (AUDITORÍA - SOLO GET)
    # =========================
    path(
        "movements/",
        MovementListView.as_view(),
        name="movement-list",
    ),
]
