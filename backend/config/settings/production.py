from .base import *  # noqa

DEBUG = False

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')  # noqa
