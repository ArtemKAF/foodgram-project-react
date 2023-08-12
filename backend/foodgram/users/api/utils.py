"""Модуль вспомогательных функций для api части приложения пользователй.

Описывает различные вспомогательные функции для использования исключительно в
api части приложения пользователей.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


def validate_recipes_limit(value):
    if value is None:
        return False
    try:
        if int(value) < 0:
            raise ValidationError(
                _('The recipes_limit parameter cannot be less than zero!')
            )
    except ValueError:
        raise ValidationError(
            _('Invalid value of the recipes_limit parameter!')
        )
    return True
