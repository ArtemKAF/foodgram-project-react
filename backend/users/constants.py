from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserRoles(TextChoices):
    USER = 'user', _('Пользователь')
    ADMIN = 'admin', _('Администратор')
