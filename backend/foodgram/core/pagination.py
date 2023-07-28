"""Модуль классов для настройки пагинации проекта Foodgram.
"""
from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """Класс пагинации по умолчанию.
    """
    page_size = 6
    page_size_query_param = 'limit'
