""" User model."""

# Django
from django.contrib.auth.models import AbstractUser

# Utilities
from apps.utils.models import BaseModel


class User(BaseModel, AbstractUser):
    """User model

    Extends from Django's Abstract User in case extra fields are needed
    Also extends from BaseModel
    """

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username
