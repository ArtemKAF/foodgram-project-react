from foodgram.recipes.api.filters import IngredientFilter, RecipeFilter
from foodgram.recipes.api.serializers import (IngredientSerializer,
                                              RecipeSerializer, TagSerializer)
from foodgram.recipes.models import Ingredient, Recipe, Tag
from rest_framework import permissions, viewsets


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
