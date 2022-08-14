from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Comment, Review, Category, Genre, Title

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации юзера."""
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message='Already exists.'
            )
        ]
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message='Already exists.'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenObtainSerializer(TokenObtainPairSerializer):
    """Сериализатор получения токена по запросу."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = self.fields['password']


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

    # def create(self, validated_data):
    #     category = Category.objects.create(**validated_data)
    #     return category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']

    # def create(self, validated_data):
    #     genre = Genre.objects.create(**validated_data)
    #     return genre


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор произведения для получения экземпляра или списка."""
    category = CategorySerializer(many=False, required=False)
    genre = GenreSerializer(many=True, required=False)
    # rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        read_only_fields = ('genre', 'category', 'rating')
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор создания экземпляра произведения."""
    genre = serializers.SlugRelatedField(many=True, write_only=True,
                                         slug_field='slug', required=False,
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(many=False, write_only=True,
                                            slug_field='slug', required=False,
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
