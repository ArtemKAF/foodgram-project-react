from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from foodgram.users.api.serializers import SubscriptionSerializer
from foodgram.users.models import Subscription
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class CastomUserViewSet(UserViewSet):

    @action(methods=('get', ), detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)


class SubscriptionViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(authors__author=self.request.user)

    @action(
        methods=('post', 'delete', ),
        detail=False,
        url_path=r'(?P<user_id>\d+)/subscribe',
        url_name='subscribe',
        permission_classes=(permissions.IsAuthenticated, )
    )
    def subscribe(self, request, *args, **kwargs):
        if request.method == 'POST':
            subscriber = request.user
            author = get_object_or_404(User, pk=kwargs.get('user_id'))
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
