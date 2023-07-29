from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / 'foodgram'

env = environ.Env()
env.read_env(str(BASE_DIR / '.env'))

DEBUG = env.bool('DEBUG', False)

E = 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
]

LOCAL_APPS = [
    'foodgram.users',
    'foodgram.recipes',
    'foodgram.core',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': env.db()
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': E,
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

LANGUAGES = [('ru', 'Russian'), ]

USE_I18N = True

TIME_ZONE = 'Europe/Moscow'

USE_TZ = True

STATIC_ROOT = str(BASE_DIR / 'staticfiles')

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

MEDIA_ROOT = str(APPS_DIR / 'media')

MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'foodgram.core.pagination.DefaultPagination',
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user': 'foodgram.users.api.serializers.CastomUserSerializer',
        'current_user': 'foodgram.users.api.serializers.CastomUserSerializer',
        'user_create':
        'foodgram.users.api.serializers.UserRegistrationSerializer',
    },
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.IsAuthenticated'],
        'user': ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
}
