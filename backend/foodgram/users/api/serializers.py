"""Модуль с сериализаторами приложения пользователей.

Описывает классы сериализаторов для преобразования данных, поступающих в
приложение отдаваемых приложением при соответствующих запросах.
"""
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from foodgram.users.models import Subscription  # isort:skip
from foodgram.core.utils.embedded import ShortRecipeSerializer  # isort:skip
from foodgram.users.api.utils import validate_recipes_limit  # isort:skip

User = get_user_model()


class GetIsSubscribedMixin:

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        if isinstance(obj, User):
            return request.user.authors.filter(author=obj).exists()
        return request.user.authors.filter(author=obj.author).exists()


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


class CustomUserSerializer(GetIsSubscribedMixin, UserSerializer):
    """Класс сериализатора для получения информации о пользователях.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        read_only_fields = ('id', )


class SubscriptionSerializer(GetIsSubscribedMixin,
                             serializers.ModelSerializer):
    """Класс сериализатора для сериализации данных о подписках.
    """

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        queryset = (
            obj.author.recipes.all()[:int(limit)]
            if validate_recipes_limit(limit)
            else obj.author.recipes.all()
        )
        return ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()

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
