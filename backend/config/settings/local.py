from .base import *  # noqa
from .base import env

SECRET_KEY = env(
    'SECRET_KEY',
    default='efN6eWqBZlpuxuvadZ8tms01iI4rGvRmsSIK2hrE8kNbhxe5wapOA7Pyj30Anz9K',
)

DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default='localhost')
