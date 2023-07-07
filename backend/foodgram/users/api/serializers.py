from djoser.serializers import UserCreateSerializer, UserSerializer
from foodgram.recipes.models import Recipe
from rest_framework import serializers


class UserRegistrationSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',
        )
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CastomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return request.user.authors.filter(author=obj).exists()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        read_only_fields = ('id', )


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time',
        )


class SubscriptionSerializer(CastomUserSerializer):
    recipes = RecipeSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    class Meta(CastomUserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
