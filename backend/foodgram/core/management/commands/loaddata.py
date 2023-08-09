"""Модуль команды управления для загрузки данных в БД.

Описывает классы для команды управления, позволяющей загружать данные об
ингредиентах и тэгах из json файла.
"""
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from foodgram.core.management.commands.constants import (  # isort:skip
    TYPES, FILE_CHOICES
)


def load_data(model, file):
    instance_list = json.load(fp=file)
    instance_list_data = []
    for instance in instance_list:
        instance_list_data.append(model(**instance))
    try:
        model.objects.bulk_create(
            instance_list_data,
            ignore_conflicts=True,
        )
    except Exception as e:
        raise e


class Command(BaseCommand):
    help = ('Команда загрузки данных по ингредиентам из файла. По умолчанию '
            'загрузка из файла "/data/ingredients.json".'
            )

    def handle(self, *args, **options):
        with open(
            file=settings.BASE_DIR / options.get('file'),
            mode='r'
        ) as file:
            try:
                load_data(TYPES.get(options.get('type')), file)
            except Exception as e:
                return self.stdout.write(f'Ошибка: {e}')
        self.stdout.write(self.style.SUCCESS('Данные загружены без ошибок.'))

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '-f',
            '--file',
            choices=FILE_CHOICES,
            required=True,
            help='Файл, из которого будут загружаться данные.',
        )
        parser.add_argument(
            'type',
            choices=TYPES.keys(),
            help='Выбор типа загружаемых данных.',
        )
        return super().add_arguments(parser)
