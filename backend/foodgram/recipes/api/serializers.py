from foodgram.recipes.models import Tag
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
