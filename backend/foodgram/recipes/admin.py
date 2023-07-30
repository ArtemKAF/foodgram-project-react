"""Модуль регистрации моделей из приложения рецептов в админ зоне проекта.

Описывает классы с настройками регистрации моделей из приложения рецептов
в админ зоне проекта для более комфортной работы с данными в моделях.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from foodgram.recipes.models import (FavoriteRecipe, Ingredient,  # isort:skip
                                     IngredientAmount, Recipe, ShoppingCart,
                                     Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс для настройки регистрации модели тэгов в админ зоне.
    """

    list_display = ('name', 'color', 'slug', )
    search_fields = ('name', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс для настройки регистрации модели ингредиента в админ зоне.
    """

    list_display = ('name', 'measurement_unit', )
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """Класс для настройки регистрации модели количества ингредиента в админ
    зоне.
    """

    list_display = ('recipe', 'ingredient', 'amount', )
    search_fields = ('recipe', 'ingredient', )


class IngredientAmountInline(admin.TabularInline):
    """Класс для настройки встроенного представления модели количества
    ингредиента.
    """

    model = IngredientAmount
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс для настройки регистрации модели рецепта в админ зоне.
    """

    def get_favorite_count(self, obj):
        return obj.favorite_recipes.all().count()

    get_favorite_count.short_description = _('Added in favorites')

    list_display = (
        'name', 'author', 'description', 'cooking_time', 'pub_date',
    )
    exclude = (
        'favorite',
    )
    readonly_fields = (
        'get_favorite_count', 'author',
    )
    list_filter = (
        'author__username', 'name', 'tags__name',
    )
    search_fields = (
        'name', 'author__username',
    )
    inlines = (IngredientAmountInline, )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Класс для настройки регистрации модели избранного рецепта в админ зоне.
    """

    ...


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Класс для настройки регистрации модели рецепта в корзине покупок в админ
    зоне.
    """

    ...
