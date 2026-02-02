from django.urls import path

from config.apps.users.views.auth_views import LoginView
from config.apps.users.views.user_views import UserCreateView
from config.apps.users.views.user_detail_view import UserDetailView
from config.apps.users.views.user_list_view import UserListView
from config.apps.users.views.user_views import TechnicianListView

urlpatterns = [
    # Auth
    path("login/", LoginView.as_view(), name="login"),

    # Crear usuario (admin)
    path("create/", UserCreateView.as_view(), name="user-create"),

    # Listar técnicos
    path("technicians/", TechnicianListView.as_view(), name="technician-list"),

    # Listar todos (admin)
    path("", UserListView.as_view(), name="user-list"),

    # Detalle / update / delete
    path("<str:pk>/", UserDetailView.as_view(), name="user-detail"),
]
