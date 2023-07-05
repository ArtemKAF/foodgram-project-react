from django.contrib import admin
from foodgram.recipes.models import Ingredient, IngredientAmount, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', )
    search_fields = ('name', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurment_unit', )
    search_fields = ('name', )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount', )
    search_fields = ('recipe', 'ingredoent', )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'description', 'cooking_time', 'pub_date',
    )
    search_fields = ('name', 'author', )
    empty_value_display = '-пусто-'
