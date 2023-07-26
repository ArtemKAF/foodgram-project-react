from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from foodgram.recipes.models import (FavoriteRecipe, Ingredient,
                                     IngredientAmount, Recipe, ShoppingCart,
                                     Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', )
    search_fields = ('name', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', )
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount', )
    search_fields = ('recipe', 'ingredient', )


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
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
    ...


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    ...
