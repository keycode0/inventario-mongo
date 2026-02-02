from rest_framework import serializers
from config.apps.users.models.user import User


class UserListSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    rol = serializers.CharField()

    def to_representation(self, instance: User):
        return {
            "id": str(instance.id),
            "username": instance.username,
            "rol": instance.rol,
        }
