from foodgram.core.utils.fields import Base64ImageField
from foodgram.recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from foodgram.users.api.serializers import CastomUserSerializer
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
            'id', 'name', 'measurement_unit',
        )
        read_only_fields = (
            'name', 'measurement_unit',
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        queryset=Ingredient.objects.all(),
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True,
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True,
    )

    class Meta:
        model = IngredientAmount
        fields = (
            'id', 'name', 'measurement_unit', 'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = CastomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True, required=True)
    is_favorited = serializers.SerializerMethodField()
    image = Base64ImageField(required=True, allow_null=False)
    text = serializers.CharField(source='description', required=True)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return request.user.favorite_recipes.filter(pk=obj.pk).exists()

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)

    @staticmethod
    def add_ingredients(instance, ingredients):
        for ingredient in ingredients:
            IngredientAmount.objects.get_or_create(
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount'],
                recipe=instance
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited', 'name',
            'image', 'text', 'cooking_time',
        )
