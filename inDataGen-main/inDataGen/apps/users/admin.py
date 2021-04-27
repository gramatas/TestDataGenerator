"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from apps.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'created', 'modified', 'deleted')
    list_filter = ('is_staff', 'created', 'modified', 'deleted')
