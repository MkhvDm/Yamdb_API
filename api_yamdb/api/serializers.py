from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор модели юзера."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role', 'confirmation_code')


class TokenObtainSerializer(TokenObtainPairSerializer):
    """Сериализатор получения токена по запросу."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = self.fields['password']
