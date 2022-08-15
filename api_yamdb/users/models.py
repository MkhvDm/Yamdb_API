from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager."""
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Username must be set')
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(username, email, **extra_fields)


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
        'email',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
