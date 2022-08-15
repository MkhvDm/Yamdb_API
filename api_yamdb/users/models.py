from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    role = models.CharField(
        'role',
        max_length=15,
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(
        'bio',
        blank=True,
    )

    confirmation_code = models.CharField(
        'confirmation_code',
        max_length=6,
        null=True,
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )

    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
