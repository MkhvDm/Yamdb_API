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
