"""Модуль регистрации моделей из приложения пользователей в админ зоне проекта.

Описывает классы с настройками регистрации моделей из приложения пользователей
в админ зоне проекта для более комфортной работы с данными в моделях.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from foodgram.users.forms import UserAdminChangeForm, UserAdminCreationForm
from foodgram.users.models import Subscription

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Класс для настройки регистрации модели пользователей в админ зоне.
    """

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            None, {'fields': ('username', 'password')}
        ),
        (
            _('Personal info'), {
                'fields': ('email', 'last_name', 'first_name', )
            }
        ),
        (
            _('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser'),
            }
        ),
        (
            _('Important dates'), {
                'fields': ('last_login', 'date_joined', )
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide', ),
                'fields': (
                    'email', 'username', 'last_name', 'first_name',
                    'password1', 'password2',
                ),
            }
        ),
    )
    list_display = (
        'last_name', 'first_name', 'username', 'email', 'is_staff',
    )
    list_editable = (
        'is_staff',
    )
    list_filter = (
        'email', 'username',
    )
    ordering = (
        'last_name', 'first_name',
    )


@admin.register(Subscription)
class CastomSubscriptionAdmin(admin.ModelAdmin):
    """Класс для  настройки регистрации модели подписок в админ зоне.
    """
    ...
