"""Модуль представлений приложения рецептов.

Описывает классы представлений для обработки запросов к проекту, связанных с
приложением рецептов.
"""
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from foodgram.recipes.api.filters import (IngredientFilter,  # isort:skip
                                          RecipeFilter)
from foodgram.recipes.api.permissions import (  # isort:skip
    IsAuthorAdminOrReadOnly
)
from foodgram.recipes.api.serializers import (  # isort:skip
    IngredientSerializer, RecipeSerializer, TagSerializer
)
from foodgram.core.utils.embedded import ShortRecipeSerializer  # isort:skip
from foodgram.recipes.constants import SHOPPING_LIST_PGF_SETTINGS  # isort:skip
from foodgram.recipes.models import (FavoriteRecipe, Ingredient,  # isort:skip
                                     IngredientAmount, Recipe, Tag,
                                     ShoppingCart)
from foodgram.recipes.utils import (  # isort:skip
    generate_shopping_list_in_pdf, create_delete_object
)


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
        return create_delete_object(
            request,
            FavoriteRecipe,
            get_object_or_404(Recipe, pk=kwargs.get('pk')),
            ShortRecipeSerializer,
            _('The recipe has already been added to favorite!'),
            args,
            kwargs
        )

    @action(
        methods=('post', 'delete', ),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def shopping_cart(self, request, *args, **kwargs):
        return create_delete_object(
            request,
            ShoppingCart,
            get_object_or_404(Recipe, pk=kwargs.get('pk')),
            ShortRecipeSerializer,
            _('The recipe has already been added to shopping cart!'),
            args,
            kwargs
        )

    @action(
        methods=('get', ),
        detail=False,
        permission_classes=(permissions.IsAuthenticated, ),
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        shopping_list = IngredientAmount.objects.filter(
            recipe__shopping_carts__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(Sum('amount'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; filename=filename')
        generate_shopping_list_in_pdf(
            shopping_list,
            response,
            SHOPPING_LIST_PGF_SETTINGS
        )
        return response
