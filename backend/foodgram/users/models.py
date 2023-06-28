from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        help_text=_(
            'Required. 254 characters or fewer.'
        ),
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        help_text=_(
            'Required. 150 characters or fewer.'
        ),
        verbose_name=_('Name'),
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        help_text=_(
            'Required. 150 characters or fewer.'
        ),
        verbose_name=_('Surname'),
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'email'

    class Meta(AbstractUser.Meta):
        ordering = ('last_name', 'first_name', )
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
