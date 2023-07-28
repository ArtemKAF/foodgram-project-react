"""Модуль команды управления для загрузки данных об ингредиентах.

Описывает классы для команды управления, позволяющей загружать данные об
ингредиентах из json файла.
"""
import json

from django.core.management.base import BaseCommand, CommandParser
from foodgram.recipes.models import Ingredient


class Command(BaseCommand):
    help = ('Команда загрузки данных по ингредиентам из файла. По умолчанию '
            'загрузка из файла "/data/ingredients.json".'
            )

    def handle(self, *args, **options):
        with open(file=options.get('file'), mode='r') as file:
            ingredients = json.load(fp=file)
            ingredients_data = []
            for ingredient in ingredients:
                ingredients_data.append(Ingredient(**ingredient))
            try:
                Ingredient.objects.bulk_create(
                    ingredients_data,
                    ignore_conflicts=True,
                )
            except Exception as e:
                self.stdout.write(f'Ошибка: {e}')

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '-f',
            '--file',
            default='data/ingredients.json',
            help='Файл, из которого будут загружаться данные.',
        )
        return super().add_arguments(parser)
