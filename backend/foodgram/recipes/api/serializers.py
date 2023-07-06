from foodgram.recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from foodgram.users.api.serializers import UserSerializer
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )
        read_only_fields = (
            'name', 'color', 'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurment_unit',
        )
        read_only_fields = (
            'name', 'measurment_unit',
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        read_only=True,
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True,
    )
    measurment_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurment_unit',
        read_only=True,
    )

    class Meta:
        model = IngredientAmount
        fields = (
            'id', 'name', 'measurment_unit', 'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    text = serializers.CharField(source='description')
    ingredients = IngredientAmountSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time',
        )

