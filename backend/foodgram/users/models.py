"""Модуль создания, настройки и управления моделями пользователей и подписок.

Описывает модели и методы для настройки и управления пользователями в проекте.
Модель пользователя основана на модели AbstractUser Django.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from foodgram.users import constants  # isort:skip
from foodgram.users.utils import get_help_text_required_max_chars  # isort:skip


class User(AbstractUser):
    """Модель пользователя.

    При создании пользователя все поля обязательны для заполнения.

    Attributes:
        email(str):
            Поле для электронная почта пользователя. Используеся для
            аутентификации.
        username(str):
            Поле для никнэйма пользователя.
        first_name(str):
            Поле для имени пользователя.
        last_name(str):
            Поле для фамилии пользователя.
        password(str):
            Поле для пароля пользователя. Используется для аутентификации.
    """
    email = models.EmailField(
        _('email'),
        max_length=constants.MAX_LENGTH_EMAIL,
        unique=True,
        blank=False,
        help_text=get_help_text_required_max_chars(
            constants.MAX_LENGTH_EMAIL
        ),
    )
    first_name = models.CharField(
        verbose_name=_('Name'),
        max_length=constants.MAX_LENGTH_FIRST_NAME,
        blank=False,
        help_text=get_help_text_required_max_chars(
            constants.MAX_LENGTH_FIRST_NAME
        ),
    )
    last_name = models.CharField(
        verbose_name=_('Surname'),
        max_length=constants.MAX_LENGTH_LAST_NAME,
        blank=False,
        help_text=get_help_text_required_max_chars(
            constants.MAX_LENGTH_LAST_NAME
        ),
    )
    password = models.CharField(
        _('Password'),
        max_length=constants.MAX_LENGTH_PASSWORD,
        help_text=get_help_text_required_max_chars(
            constants.MAX_LENGTH_PASSWORD
        ),
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'email'

    class Meta(AbstractUser.Meta):
        ordering = ('last_name', 'first_name', )
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписок пользователей друг на друга.

    При создании подписки все поля обязательны для заполнения.

    Attributes:
        author(int):
            Поле ForeignKey на пользователя, на которого подписываются.
        subscriber(int):
            Поле ForeignKey на пользователя, который подписывается.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name=_('Author'),
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name=_('Subscriber'),
    )

    class Meta:
        ordering = ('id', )
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'subscriber', ),
                name='%(app_label)s_%(class)s_unique_relationships',
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='%(app_label)s_%(class)s_prevent_subscrubing_yourself',
            ),
        ]

    def __str__(self):
        return (
            f'{self.subscriber.username} ' + _('subscribed to')
            + f' {self.author.username}'
        )
