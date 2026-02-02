from rest_framework import serializers
from config.apps.users.models.user import User
from config.apps.users.permissions.roles import Roles


class UserUpdateSerializer(serializers.Serializer):
    """
    Permite actualizar rol y/o password de un usuario.
    - username NO es editable
    - admin NO puede ser modificado
    """

    rol = serializers.ChoiceField(
        choices=[role.value for role in Roles],
        required=False
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=6
    )

    def validate(self, data):
        user = self.instance

        # 🔒 No modificar admin
        if user.rol == Roles.ADMIN.value:
            raise serializers.ValidationError(
                "No se puede modificar el usuario administrador"
            )

        return data

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
