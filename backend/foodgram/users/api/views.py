from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from foodgram.users.api.serializers import SubscriptionSerializer
from foodgram.users.models import Subscription
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

User = get_user_model()


class CastomUserViewSet(UserViewSet):
    ...

class SubscriptionListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return User.objects.filter(subscribers__subscriber=self.request.user)


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
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
