# Generated by Django 4.2.2 on 2023-07-05 03:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_ingredient'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ingredient amount',
                'verbose_name_plural': 'Amounts of ingredients',
                'ordering': ('id',),
                'default_related_name': 'ingredients_amount',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(verbose_name='Время приготовления, мин')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='Изображение')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('favorite', models.ManyToManyField(blank=True, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Лайкнувшие')),
                ('ingredient', models.ManyToManyField(through='recipes.IngredientAmount', to='recipes.ingredient', verbose_name='Ингредиент')),
                ('tag', models.ManyToManyField(to='recipes.tag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('-pub_date',),
                'default_related_name': 'recipes',
            },
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
