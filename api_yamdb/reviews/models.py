from django.db import models
from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Category(models.Model):
    """Модель категории произведения."""
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Title(models.Model):
    """Модель произведения."""
    name = models.TextField()
    year = models.IntegerField()
    description = models.CharField(
        max_length=250,
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category, blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre, blank=True,
        through='TitleGenre',
        related_name='titles'
    )


class TitleGenre(models.Model):
    """Модель для связи между произведениями и их жанрами."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    """Модель рецензии на произведение."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField('Дата рецензии', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]

    def __str__(self):
        return f'{self.text[:30]}...'


class Comment(models.Model):
    """Модель комментария к рецензии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
