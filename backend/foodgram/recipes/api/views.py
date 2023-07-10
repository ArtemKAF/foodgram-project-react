from foodgram.recipes.api.serializers import (IngredientSerializer,
                                              RecipeSerializer, TagSerializer)
from foodgram.recipes.models import Ingredient, Recipe, Tag
from rest_framework import permissions, viewsets

#from rest_framework.decorators import action
#from rest_framework.response import Response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
