"""Модуль констант для приложения рецептов.

Описывает различные константы для использования в приложении рецептов.
"""
from django.conf import settings
from reportlab.lib.pagesizes import A4

MAX_LENGTH_CHARFIELD = 200

SHOPPING_LIST_PDF_SETTINGS = {
    'PAGE_SIZE': A4,
    'FONT_NAME': 'DejaVuSans',
    'FONT_FILE': settings.BASE_DIR / 'data/DejaVuSans.ttf',
    'FONT_SIZE_IN_PT': 0.99,
    'TOP_BORDER': 20,
    'HEADER_FONT_SIZE': 20,
    'INDENTATION_HEADER': 230,
    'HEADER_SPACING': 16,
    'TEXT_FONT_SIZE': 12,
    'INDENTATION_LIST': 60,
    'LINE_SPACING': 8,
    'BOTTOM_BORDER': 30,
}
