from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=150,
        unique=True,
        blank=False,
        db_index=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Альтернативное название',
        max_length=150,
        unique=True,
        blank=False,
        db_index=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=250,
        blank=False,
        db_index=True,
    )
    measurment_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
        blank=False,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self) -> str:
        return self.name
