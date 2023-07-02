from foodgram.recipes.api.serializers import TagSerializer
from foodgram.recipes.models import Tag
from rest_framework import permissions, viewsets


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )
