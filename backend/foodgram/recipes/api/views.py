from foodgram.recipes.api.serializers import (IngredientSerializer,
                                              TagSerializer)
from foodgram.recipes.models import Ingredient, Tag
from rest_framework import permissions, viewsets


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny, )
