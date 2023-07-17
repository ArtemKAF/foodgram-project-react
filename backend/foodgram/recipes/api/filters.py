from django_filters import rest_framework
from foodgram.recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(rest_framework.FilterSet):
    author = rest_framework.NumberFilter(
        field_name='author__id',
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', )
