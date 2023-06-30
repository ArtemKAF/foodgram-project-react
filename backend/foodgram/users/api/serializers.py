from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import SerializerMethodField


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
    is_subscribed = SerializerMethodField()

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


class SubscriptionSerializer(CastomUserSerializer):
    class Meta(CastomUserSerializer.Meta):
        ...
