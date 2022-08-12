from rest_framework import serializers

from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = self.fields['password']
