from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class Admin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Persanal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
    )
    list_editable = (
        'is_staff',
    )
    list_filter = (
        'email', 'username',
    )
