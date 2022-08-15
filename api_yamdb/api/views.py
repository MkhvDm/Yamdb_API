import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404, RetrieveUpdateAPIView)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedAndAdmin
from .serializers import (CommentSerializer, ReviewSerializer,
                          SignUpSerializer, TokenObtainSerializer,
                          UserSerializer)

User = get_user_model()


class SignUpAPIView(CreateAPIView):
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
        if serializer.is_valid(raise_exception=True):
            confirmation_code = self.generate_confirmation_code()
            email = serializer.validated_data['email']
            serializer.validated_data['confirmation_code'] = confirmation_code
            serializer.save()
            self.send_confirmation_code_to_mail(email, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
        response = {'message': 'не верный код.'}
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


class UsersAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndAdmin]
    pagination_class = LimitOffsetPagination
    search_fields = ('=username',)


class ProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndAdmin]
    lookup_field = 'username'


class SelfProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
