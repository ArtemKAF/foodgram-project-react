"""Модуль классов прав доступа для приложения рецептов.

Описывает классы настройки прав доступа к методам и объектам в приложениии
рецептов.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorAdminOrReadOnly(BasePermission):
    """Класс прав доступа к изменению объектов только автору/администратору.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.is_superuser
            )
        )
