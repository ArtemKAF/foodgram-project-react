from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        help_text=_(
            'Обязательное поле. Не более 254 символов.'
        ),
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        help_text=_(
            'Обязательное поле. Не более 150 символов.'
        ),
        verbose_name=_('Имя'),
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        help_text=_(
            'Обязательное поле. Не более 150 символов.'
        ),
        verbose_name=_('Фамилия'),
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'email'

    class Meta(AbstractUser.Meta):
        ordering = ('last_name', 'first_name', )
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
