"""Модуль с сериализаторами приложения рецептов.

Описывает классы сериализаторов для преобразования данных, поступающих в
приложение отдаваемых приложением при соответствующих запросах.
"""


from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from foodgram.recipes.models import (Ingredient,  # isort:skip
                                     IngredientAmount, Recipe, Tag,
                                     FavoriteRecipe, ShoppingCart)
from foodgram.users.api.serializers import CustomUserSerializer  # isort:skip
from foodgram.recipes.utils import (is_in_something,  # isort:skip
                                    validate_unique_items)

class TagSerializer(serializers.ModelSerializer):
    """Класс сериализатора для модели тэгов.
    """

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )
        read_only_fields = (
            'name', 'color', 'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Класс сериализатора для модели ингредиентов.
    """

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )
        read_only_fields = (
            'name', 'measurement_unit',
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Класс сериализатора для модели количества ингредиента.
    """

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
    """Класс сериализатора для модели рецептов.
    """

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True, required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True, allow_null=False)
    text = serializers.CharField(source='description', required=True)

    def get_is_favorited(self, obj):
        return is_in_something(self, FavoriteRecipe, obj=obj)

    def get_is_in_shopping_cart(self, obj):
        return is_in_something(self, ShoppingCart, obj=obj)

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)

    def add_ingredients(self, instance, ingredients):
        for ingredient in ingredients:
            IngredientAmount.objects.get_or_create(
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount'],
                recipe=instance,
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            IngredientAmount.objects.filter(recipe=instance).delete()
            self.add_ingredients(instance, ingredients)
        super().update(instance, validated_data)
        return instance

    def validate(self, data):
        errors = {}
        ingredients = validate_unique_items(
            data.get('ingredients'),
            'ingredient'
        )
        if ingredients:
            errors['multiple'] = _(
                '%(ingredients)s are found more than once!'
            ) % {'ingredients': ingredients}
        if self.context.get('request').method == 'POST':
            if Recipe.objects.filter(
                name=data.get('name'),
                author=self.context.get('request').user.pk
            ).exists():
                errors['exists'] = _(
                    'Do you already have a recipe with this name!'
                )
        if errors:
            raise serializers.ValidationError(errors)
        return super(RecipeSerializer, self).validate(data)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )
