import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, ReviewSerializer,
                          SignUpSerializer, TokenObtainSerializer)

User = get_user_model()


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    pass


class SignUpViewSet(CreateUserViewSet):
    """Создать пользователя и отправить код на почту."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def generate_confirmation_code(self):
        return random.randrange(111111, 999999, 6)

    def send_confirmation_code_to_mail(self, email, confirmation_code):
        subject = 'YaMDB confirmation code'
        message = (
            'Используйте этот код:\n'
            f'{confirmation_code}\n'
            'для получения токена.'
        )
        from_email = 'reg@yamdb.com'
        recipient_list = [email, ]
        send_mail(subject, message, from_email, recipient_list)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = self.generate_confirmation_code()
            email = serializer.validated_data['email']
            serializer.validated_data['confirmation_code'] = confirmation_code
            serializer.save()
            self.send_confirmation_code_to_mail(email, confirmation_code)
            response = {'message': 'проверьте почту.'}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class TokenObtainView(TokenObtainPairView):
    """Получить токен доступа по коду из письма."""
    serializer_class = TokenObtainSerializer

    def get_queryset(self):
        return get_object_or_404(
            User, username=self.request.data.get('username')
        )

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        user = self.get_queryset()
        if user.confirmation_code == request.data.get('confirmation_code'):
            response = {'token': self.get_token(user)}
            return Response(response, status=status.HTTP_200_OK)
        response = {'message': 'неверный код.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
