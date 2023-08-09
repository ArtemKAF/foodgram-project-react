from foodgram.recipes.models import Ingredient, Tag

TYPES = {
    'ingredient': Ingredient,
    'tag': Tag,
}
FILE_CHOICES = (
    'data/ingredients.json',
    'data/tags.json',
)
