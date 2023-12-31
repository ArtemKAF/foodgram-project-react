"""Модуль классов, реализующих фильтрацию данных в результатах запросов.

Описывает классы с настройками фильтров для наборов данных в приложении
рецептов.
"""
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from foodgram.recipes.models import Recipe, Tag  # isort: skip


def filtering_recipes(self, queryset, value, filter_parameters):
    if self.request.user.is_authenticated and value is not None:
        if value:
            return queryset.filter(**filter_parameters)
        else:
            return queryset.exclude(**filter_parameters)
    return queryset


class IngredientFilter(SearchFilter):
    """Класс настройки фильтра для поиска ингредиента по имени.
    """

    search_param = 'name'


class RecipeFilter(rest_framework.FilterSet):
    """Класс настройки фильтра для рецептов.
    """

    author = rest_framework.NumberFilter(
        field_name='author__id',
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = rest_framework.BooleanFilter(
        method='is_favorited_filter',
        label=_('Is favorited'),
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='is_in_shopping_cart_filter',
        label=_('Is in shopping cart'),
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', )

    def is_favorited_filter(self, queryset, name, value):
        return filtering_recipes(
            self,
            queryset,
            value,
            {'favorite_recipes__user': self.request.user}
        )

    def is_in_shopping_cart_filter(self, queryset, name, value):
        return filtering_recipes(
            self,
            queryset,
            value,
            {'shopping_carts__user': self.request.user}
        )
