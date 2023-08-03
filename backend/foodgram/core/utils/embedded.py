from foodgram.recipes.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Класс сериализатора для получения информации о рецептах.

    Необходим для формирования данных о рецептах авторов, на которых подписан
    пользователь.
    """

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time',
        )
        read_only_fields = (
            'id', 'name', 'image', 'cooking_time',
        )
