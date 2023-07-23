from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from foodgram.recipes.api.filters import IngredientFilter, RecipeFilter
from foodgram.recipes.api.serializers import (IngredientSerializer,
                                              RecipeSerializer,
                                              ShortRecipeSerializer,
                                              TagSerializer)
from foodgram.recipes.models import Ingredient, Recipe, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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
    queryset = Recipe.objects.all().select_related(
        'author'
    ).prefetch_related(
        'tags', 'ingredients',
    )
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny, )
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, args=args, kwargs=kwargs)

    @action(
        methods=('post', 'delete', ),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs.get('pk'))
        favorited = request.user
        if request.method == 'POST':
            try:
                recipe.favorite_recipes.create(
                    recipe=recipe,
                    user=favorited,
                )
            except IntegrityError as e:
                return Response(
                    {'errors': e.args},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe.favorite_recipes.filter(user=favorited).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
