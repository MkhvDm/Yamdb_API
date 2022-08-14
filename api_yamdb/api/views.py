import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import mixins, status, viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

from .permissions import (IsAuthorOrReadOnly, IsAdminOrReadOnly, IsModerator, 
                          IsAdmin, IsAuthor, ReadOnly)
from .serializers import (CommentSerializer, ReviewSerializer,
                          SignUpSerializer, TokenObtainSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleViewSerializer, TitlePostSerializer)
from .filters import TitlesFilter

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
            return Response(response, status=status.HTTP_200_OK)
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
            return Response(response, status=status.HTTP_201_CREATED)
        response = {'message': 'неверный код.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsModerator | IsAdmin | IsAuthor | ReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsModerator | IsAdmin | IsAuthor | ReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user,
                        review=review)


class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet
                        ):
    """Вьюсет для Категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet
                    ):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlePostSerializer
        return TitleViewSerializer
