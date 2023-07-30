"""Модуль представлений приложения пользователей.

Описывает классы представлений для обработки запросов к проекту, связанных с
приложением пользователй.
"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from foodgram.users.api.serializers import SubscriptionSerializer  # isort:skip
from foodgram.users.models import Subscription  # isort:skip

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Класс представления пользователей.

    Отвечает за обработку запросов для работы с пользователями. Унаследован от
    класса представления пользователей Django.
    """

    ...


class SubscriptionListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Класс представления списка подписок пользователей.

    Отвечает за обработку запросов на получения списка подписок пользователей.
    """

    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return User.objects.filter(subscribers__subscriber=self.request.user)


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """Класс представления создания и удаления подписок пользователей.

    Отвечает за обработку запросов на создание/удаление подписки на
    пользователя.
    """

    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, pk=user_id)

        instance = Subscription.objects.filter(
            subscriber=request.user, author=author)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
