"""Модуль представлений приложения пользователей.

Описывает классы представлений для обработки запросов к проекту, связанных с
приложением пользователй.
"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from foodgram.users.api.serializers import SubscriptionSerializer  # isort:skip
from foodgram.users.models import Subscription  # isort:skip

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Класс представления пользователей.

    Отвечает за обработку запросов для работы с пользователями. Унаследован от
    класса представления пользователей Django.
    """
    @action(
        methods=('get', ),
        detail=False,
        url_path='subscriptions',
        url_name='subscriptions',
        serializer_class=SubscriptionSerializer,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def subscriptions(self, request):
        queryset = self.filter_queryset(
            User.objects.filter(subscribers__subscriber=self.request.user)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('post', 'delete', ),
        detail=True,
        url_path='subscribe',
        url_name='subscribe',
        serializer_class=SubscriptionSerializer,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def subscribe(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        instance = get_object_or_404(
            Subscription,
            author=kwargs.get('id'),
            subscriber=request.user,
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
