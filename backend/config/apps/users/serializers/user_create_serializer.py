from rest_framework import serializers
from config.apps.users.models.user import User
from config.apps.users.permissions.roles import Roles


class UserCreateSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    username = serializers.CharField(min_length=3, max_length=50)
    password = serializers.CharField(write_only=True, min_length=6)
    rol = serializers.ChoiceField(
        choices=[role.value for role in Roles]
    )

    def validate_username(self, value):
        if User.objects(username=value).first():
            raise serializers.ValidationError(
                "El nombre de usuario ya existe"
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
