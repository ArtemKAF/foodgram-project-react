"""Модуль с сериализаторами приложения пользователей.

Описывает классы сериализаторов для преобразования данных, поступающих в
приложение отдаваемых приложением при соответствующих запросах.
"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from foodgram.recipes.models import Recipe  # isort:skip
from foodgram.users.models import Subscription  # isort:skip

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    """Класс сериализатора для создания пользователей.
    """

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',
        )
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomUserSerializer(UserSerializer):
    """Класс сериализатора для получения информации о пользователях.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        read_only_fields = ('id', )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return request.user.authors.filter(author=obj).exists()


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


class SubscriptionSerializer(CustomUserSerializer):
    """Класс сериализатора для сериализации данных о подписках.
    """

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = (
            'email', 'username', 'first_name', 'last_name',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if limit is not None:
            queryset = queryset[:int(limit)]
        return RecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    def create(self, validated_data):
        Subscription.objects.create(**validated_data)
        author = get_object_or_404(User, pk=validated_data.get('author_id'))
        return author

    def validate(self, data):
        errors = {}
        request = self.context.get('request')
        author_id = int(request.parser_context.get('kwargs').get('id'))
        subscriber_id = request.user.pk
        if author_id == subscriber_id:
            errors['yourself'] = _('You can not subscribe to yourself!')
        if Subscription.objects.filter(
            author_id=author_id,
            subscriber_id=subscriber_id
        ).exists():
            errors['exist'] = _('You are already subscribed to this user!')
        if errors:
            raise serializers.ValidationError(errors)
        data = {'author_id': author_id, 'subscriber_id': subscriber_id}
        return super(SubscriptionSerializer, self).validate(data)
