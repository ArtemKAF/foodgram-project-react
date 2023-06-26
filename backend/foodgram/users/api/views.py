from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

#from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
#from rest_framework.viewsets import GenericViewSet

#from .serializers import UserSerializer

User = get_user_model()


class CastomUserViewSet(UserViewSet):
    ...
