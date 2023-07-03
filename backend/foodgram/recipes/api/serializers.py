from foodgram.recipes.models import Ingredient, Tag
from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )
        read_only_fields = (
            'name', 'color', 'slug',
        )


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurment_unit',
        )
        read_only_fields = (
            'name', 'measurment_unit',
        )
