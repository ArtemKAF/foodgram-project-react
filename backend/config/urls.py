from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('users/', include('foodgram.users.urls', namespace='users')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/', include('config.api_router')),
]
