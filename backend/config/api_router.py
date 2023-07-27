from django.conf import settings
from django.urls import include, path
from foodgram.recipes.api.views import (IngredientViewSet, RecipeViewSet,
                                        TagViewSet)
from foodgram.users.api.views import (CastomUserViewSet,
                                      SubscriptionListViewSet,
                                      SubscriptionViewSet)
from rest_framework.routers import DefaultRouter, SimpleRouter

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
router.register('users', CastomUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

app_name = 'api'
urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
