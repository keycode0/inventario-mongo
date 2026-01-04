from django.urls import path
from config.apps.users.views.auth_views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
]
