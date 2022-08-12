from django.shortcuts import render
from reviews.models import Category, Comment, Genre, TitleGenre, Title, Review
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
