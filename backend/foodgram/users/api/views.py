from djoser.views import UserViewSet
from rest_framework.decorators import action


class CastomUserViewSet(UserViewSet):

    @action(methods=('get', ), detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)
