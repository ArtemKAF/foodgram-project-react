"""Модуль вспомогательных функций для приложения пользователй.

Описывает различные вспомогательные функции для использования в приложении
пользователей.
"""

from django.utils.translation import gettext_lazy as _


def get_help_text_required_max_chars(value):
    return _(
        'Required. %(value)s characters or fewer.'
    ) % {'value': value}
