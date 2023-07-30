from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from foodgram.recipes.api.views import (IngredientViewSet,  # isort:skip
                                        RecipeViewSet,
                                        TagViewSet)
from foodgram.users.api.views import (CustomUserViewSet,  # isort: skip
                                      SubscriptionListViewSet,
                                      SubscriptionViewSet)


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(
    'users/subscriptions',
    SubscriptionListViewSet,
    basename='subscribtions'
)
router.register(
    r'users/(?P<user_id>\d+)/subscribe',
    SubscriptionViewSet,
    basename='subscribe'
)
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

app_name = 'api'
urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
