from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
        validators=[
            RegexValidator(
                regex=r'^#[0-9a-fA-F]{6}$',
                message=_('%(value)s is not correct HEX color.'),
            ),
        ],
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
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
        blank=False,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit', ),
                name='%(app_label)s_%(class)s_unique_ingredients',
            ),
        )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=250,
        blank=False,
        db_index=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин',
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
        verbose_name='Изображение',
        blank=False,
        upload_to='recipes/',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        blank=False,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        blank=False,
        on_delete=models.CASCADE,
    )
    favorite = models.ManyToManyField(
        User,
        verbose_name='Лайкнувшие',
        related_name='favorite_recipes',
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        default_related_name = 'recipes'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество',
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

    def __str__(self):
        return (
            f'{self.amount} {self.ingredient.measurement_unit} '
            f'{self.ingredient.name} в {self.recipe.name}'
        )
