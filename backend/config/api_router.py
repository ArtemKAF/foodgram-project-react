from django.conf import settings
from django.urls import include, path
from foodgram.recipes.api.views import (IngredientViewSet, RecipeViewSet,
                                        TagViewSet)
from foodgram.users.api.views import CastomUserViewSet, SubscriptionViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(
    'users', SubscriptionViewSet, basename='subscriptions')
router.register('users', CastomUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

app_name = 'api'
urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
