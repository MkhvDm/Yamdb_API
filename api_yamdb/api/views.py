import random

from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail

from users.models import User
from .serializers import CustomTokenObtainPairSerializer, SignUpSerializer


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    pass


class SignUpViewSet(CreateUserViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def generate_confirmation_code(self):
        return int(''.join([str(random.randint(0, 10)) for _ in range(6)]))

    def send_confirmation_code_to_mail(self, email, code):
        subject = 'YaMDB код верификации'
        message = (
            f'Используйте этот код:\n{code}\n'
            'для получения токена.'
        )
        from_email = 'reg@yamdb.com'
        recipient_list = [email, ]
        send_mail(subject, message, from_email, recipient_list)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            code = self.generate_confirmation_code()
            email = serializer.validated_data['email']
            print(serializer.validated_data)
            #pair = Confirmation.objects.create(confirmation_code=code, username=email)
            #pair.save()
            self.send_confirmation_code_to_mail(email, code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer