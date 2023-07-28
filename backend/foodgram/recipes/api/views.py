"""Модуль представлений приложения рецептов.

Описывает классы представлений для обработки запросов к проекту, связанных с
приложением рецептов.
"""
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from foodgram.recipes.api.filters import IngredientFilter, RecipeFilter
from foodgram.recipes.api.permissions import IsAuthorAdminOrReadOnly
from foodgram.recipes.api.serializers import (IngredientSerializer,
                                              RecipeSerializer,
                                              ShortRecipeSerializer,
                                              TagSerializer)
from foodgram.recipes.api.utils import generate_shopping_list_in_pdf
from foodgram.recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления тэгов.

    Отвечает за обработку запросов для работы с тэгами.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления ингредиентов.

    Отвечает за обработку запросов для работы с ингредиентами.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    """Класс представления рецептов.

    Отвечает за обработку запросов для работы с рецептами.
    """

    queryset = Recipe.objects.all().select_related(
        'author'
    ).prefetch_related(
        'tags', 'ingredients',
    )
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorAdminOrReadOnly, )
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=('post', 'delete', ),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs.get('pk'))
        favorited = request.user
        if request.method == 'POST':
            if recipe.favorite_recipes.filter(user=favorited).exists():
                return Response(
                    {
                        'errors':
                        _('The recipe has already been added to favorite!')
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe.favorite_recipes.create(user=favorited)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe.favorite_recipes.filter(user=favorited).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('post', 'delete', ),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def shopping_cart(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs.get('pk'))
        buyer = request.user
        if request.method == 'POST':
            if recipe.shopping_carts.filter(buyer=buyer).exists():
                return Response(
                    {
                        'errors':
                        _('The recipe has already been added to shopping cart!')
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe.shopping_carts.create(buyer=buyer)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe.shopping_carts.filter(buyer=buyer).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('get', ),
        detail=False,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        shopping_list = IngredientAmount.objects.filter(
            recipe__shopping_carts__buyer=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(Sum('amount'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; filename=filename')
        generate_shopping_list_in_pdf(shopping_list, response)        
        return response
