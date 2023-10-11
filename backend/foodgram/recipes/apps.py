from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodgram.recipes'
    verbose_name = _('Recipes')

    def ready(self):
        from . import signals  # noqa: F401,
        return super().ready()
