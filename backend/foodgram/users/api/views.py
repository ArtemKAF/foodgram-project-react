from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from foodgram.users.api.serializers import SubscriptionSerializer
from foodgram.users.models import Subscription
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class CastomUserViewSet(UserViewSet):
    ...


class SubscriptionViewSet(viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(authors__author=self.request.user)

    @action(
        methods=('get', ),
        detail=False,
        url_name='list'
    )
    def subscriptions(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=('post', 'delete', ),
        detail=False,
        url_path=r'(?P<id>[^/.]+)/subscribe',
        url_name='subscribe',
        permission_classes=(permissions.IsAuthenticated, )
    )
    def subscribe(self, request, *args, **kwargs):
        subscriber = request.user
        author = get_object_or_404(User, pk=kwargs.get('id'))
        subscription = Subscription.objects.filter(
            subscriber=subscriber,
            author=author
        )
        if request.method == 'POST':
            subscriber = request.user
            author = get_object_or_404(User, pk=kwargs.get('id'))
            subscription = Subscription.objects.filter(
                subscriber=subscriber,
                author=author
            )
            if (
                not subscription.exists()
                and subscriber != author
            ):
                Subscription.objects.create(
                    author=author,
                    subscriber=subscriber
                )
                serializer = SubscriptionSerializer(
                    author,
                    context={'request': request}
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                errors = {}
                if subscription.exists():
                    errors['exist'] = 'Подписка уже осуществлена.'
                if subscriber == author:
                    errors['yourself'] = 'Нельзя подписаться на самого себя.'
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'not exists': 'Подписка отсутствует.'},
            status=status.HTTP_400_BAD_REQUEST
        )
