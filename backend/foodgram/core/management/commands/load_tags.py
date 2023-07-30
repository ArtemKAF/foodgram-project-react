"""Модуль команды управления для загрузки данных о тэгах.

Описывает классы для команды управления, позволяющей загружать данные о тэгах
из json файла.
"""
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from foodgram.recipes.models import Tag  # isort: skip


class Command(BaseCommand):
    help = ('Команда загрузки данных по тэгам из файла. По умолчанию '
            'загрузка из файла "/data/tags.json".'
            )

    def handle(self, *args, **options):
        with open(file=options.get('file'), mode='r') as file:
            tags = json.load(fp=file)
            tags_data = []
            for tag in tags:
                tags_data.append(Tag(**tag))
            try:
                Tag.objects.bulk_create(
                    tags_data,
                    ignore_conflicts=True,
                )
            except Exception as e:
                self.stdout.write(f'Ошибка: {e.args}')

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '-f',
            '--file',
            default=settings.BASE_DIR / 'data/tags.json',
            help='Файл, из которого будут загружаться данные.',
        )
        return super().add_arguments(parser)
