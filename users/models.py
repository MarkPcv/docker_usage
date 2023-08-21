from django.contrib.auth.models import AbstractUser
from django.db import models

from habit_tracker.models import NULLABLE


class UserRoles(models.TextChoices):
    MEMBER = 'member'
    MODERATOR = 'moderator'


class User(AbstractUser):
    """
    Stores a single user entry for authenticated users.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    phone = models.CharField(max_length=35, verbose_name='phone',
                             **NULLABLE)

    # Role for permissions
    role = models.CharField(max_length=9, choices=UserRoles.choices,
                            default=UserRoles.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []