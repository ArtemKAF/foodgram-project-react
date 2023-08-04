"""Модуль создания, настройки и управления моделями в приложении рецептов.

Описывает модели и методы для настройки и управления тэгами, ингредиентами и
количеством ингредиентов, а также избранными рецептами и корзинами покупок.
"""
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from foodgram.recipes import constants  # isort:skip

User = get_user_model()


class Tag(models.Model):
    """Модель тэга.

    При создании тэга все поля обязательны для заполнения.

    Attributes:
        name(str):
            Поле для названия тэга.
        color(str):
            Поле для цвета тэга в HEX формате.
        slug(str):
            Поле для альтернативного названия тэга.
    """

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=constants.MAX_LENGTH_TAG_NAME,
        unique=True,
        blank=False,
        db_index=True,
    )
    color = ColorField(
        verbose_name=_('Color'),
        unique=True,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=constants.MAX_LENGTH_SLUG,
        unique=True,
        blank=False,
        db_index=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'color', ),
                name='%(app_label)s_%(class)s_unique_tags_color',
            ),
        )

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента.

    При создании ингредиента все поля обязательны для заполнения.

    Attributes:
        name(str):
            Поле для названия ингредиента.
        measurement_unit(str):
            Поле для единицы измерения количества ингредиента.
    """

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=constants.MAX_LENGTH_INGREDIENT_NAME,
        blank=False,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name=_('Measurement unit'),
        max_length=constants.MAX_LENGTH_MEASUREMENT_UNIT,
        blank=False,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit', ),
                name=(
                    '%(app_label)s_%(class)s_unique_ingredient_measurment_unit'
                ),
            ),
        )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецепта.

    При создании рецепта все поля обязательны для заполнения. Поле pub_date
    заполняется автоматически.

    Attributes:
        name(str):
            Поле для названия рецепта.
        description(str):
            Поле для подробного описания рецепта.
        cooking_time(int):
            Поле для времени приготовления блюда по рецепту.
        image(str):
            Поле для ссылки на изображение для рецепта.
        pub_date(DATETIME):
            Поле для времени создания рецепта.
        tags(int):
            Поле ManyToManyField на тэги для рецепта.
        author(int):
            Поле ForeignKey на пользователя, который является автором рецепта.
    """

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=constants.MAX_LENGTH_RECIPE_NAME,
        blank=False,
        db_index=True,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Cooking time, min'),
        blank=False,
        validators=(
            MinValueValidator(
                limit_value=1,
                message=_(
                    'The cooking time can not be less than one minute.'
                )
            ),
        )
    )
    image = models.ImageField(
        verbose_name=_('Image'),
        blank=False,
        upload_to='recipes/',
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Date of publishing'),
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        blank=False,
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Author'),
        blank=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        default_related_name = 'recipes'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author', ),
                name='%(app_label)s_%(class)s_unique_recipe_from_author',
            ),
        )

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    """Модель избранного рецепта.

    При создании избранного рецепта все поля обязательны для заполнения.

    Attributes:
        user(int):
            Поле ForeignKey на пользователя, у которого рецепт в избранном.
        recipe(int):
            Поле ForeignKey на рецепт, добавленный в избранное.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('Recipe'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Favorite recipe')
        verbose_name_plural = _('Favorite recipes')
        default_related_name = 'favorite_recipes'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe', ),
                name='%(app_label)s_%(class)s_unique_recipe_in_favorite',
            ),
        )

    def __str__(self):
        return _(
            'Recipe %(recipe)s in the %(favorited)s favorites'
        ) % {'recipe': self.recipe.name, 'favorited': self.user.username}


class IngredientAmount(models.Model):
    """Модель количества ингредиента.

    При создании количества ингредиента все поля обязательны для заполнения.

    Attributes:
        ingredient(int):
            Поле ForeignKey на ингредиент.
        recipe(int):
            Поле ForeignKey на рецепт.
        amount(int):
            Поле для количества ингредиента.
    """

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('Ingredient'),
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('Recipe'),
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    amount = models.SmallIntegerField(
        verbose_name=_('Amount'),
        blank=False,
        validators=(
            MinValueValidator(
                limit_value=1,
                message=_(
                    'The amount of the ingredient can not be less than one.'
                )
            ),
        )
    )

    class Meta:
        ordering = ('id', )
        verbose_name = _('Ingredient amount')
        verbose_name_plural = _('Amounts of ingredients')
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe', ),
                name='%(app_label)s_%(class)s_unique_ingredient_in_recipe',
            ),
        )

    def __str__(self):
        return (
            f'{self.ingredient.name} {self.amount} '
            f'{self.ingredient.measurement_unit} ' + _('in')
            + f' {self.recipe.name}'
        )


class ShoppingCart(models.Model):
    """Модель рецепта в корзине покупок.

    При создании рецепта в корзине покупок все поля обязательны для заполнения.

    Attributes:
        user(int):
            Поле ForeignKey на пользователя, добавившего рецепт в корзину
            покупок.
        recipe(int):
            Поле ForeignKey на рецепт, добавленный в корзину покупок.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name=_('Buyer'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name=_('Recipe'),
    )

    class Meta:
        ordering = ('id', )
        verbose_name = _('Shopping cart')
        verbose_name_plural = _('Shopping carts')
        default_related_name = 'shopping_carts'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe', ),
                name=('%(app_label)s_%(class)s_unique_recipe_from_user'),
            ),
        )

    def __str__(self):
        return _(
            'Recipe %(recipe)s in shopping cart from %(user)s'
        ) % {'recipe': self.recipe.name, 'user': self.user.username}
