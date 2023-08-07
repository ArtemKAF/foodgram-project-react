"""Модуль вспомогательных функций для приложения рецептов.

Описывает различные вспомогательные функции для использования в приложении
рецептов.
"""

from django.utils.translation import gettext as _
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status
from rest_framework.response import Response


def generate_shopping_list_in_pdf(ingredients, filename, settings):
    try:
        registerFont(
            TTFont(
                settings.get('FONT_NAME'),
                settings.get('FONT_FILE'),
                'utf-8'
            )
        )
    except Exception as e:
        return Response(
            {'errors': e.args},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    heading_height = (
        settings.get('HEADER_FONT_SIZE') * settings.get('FONT_SIZE_IN_PT')
    )
    text_height = (
        settings.get('TEXT_FONT_SIZE') * settings.get('FONT_SIZE_IN_PT')
    )
    line_spacing = (
        settings.get('LINE_SPACING') * settings.get('FONT_SIZE_IN_PT')
    )
    page = Canvas(filename=filename, pagesize=settings.get('PAGE_SIZE'))
    page.setFont(settings.get('FONT_NAME'), settings.get('HEADER_FONT_SIZE'))
    page.drawString(
        x=settings.get('INDENTATION_HEADER'),
        y=(settings.get('PAGE_SIZE')[1] - settings.get('TOP_BORDER')
            - heading_height),
        text=_('Shopping list:'),
    )
    page.setFont(settings.get('FONT_NAME'), settings.get('TEXT_FONT_SIZE'))
    height = (
        settings.get('PAGE_SIZE')[1] - settings.get('TOP_BORDER')
        - heading_height - settings.get('HEADER_SPACING') - text_height
    )
    for ingredient in ingredients:
        page.drawString(
            settings.get('INDENTATION_LIST'),
            height,
            text=(
                '- {ingredient} ({measurement_unit}) -- {amount}'.format(
                    ingredient=ingredient.get('ingredient__name').capitalize(),
                    measurement_unit=ingredient.get(
                        'ingredient__measurement_unit'
                    ),
                    amount=ingredient.get('amount__sum'),
                )
            ))
        height -= (text_height + line_spacing)
        if height <= settings.get('BOTTOM_BORDER'):
            page.showPage()
            page.setFont(
                settings.get('FONT_NAME'),
                settings.get('TEXT_FONT_SIZE')
            )
            height = (
                settings.get('PAGE_SIZE')[1] - text_height
                - settings.get('TOP_BORDER')
            )
    page.save()


def is_in_something(serializer, model, obj, *args, **kwargs):
    request = serializer.context.get('request')
    if request is None or not request.user.is_authenticated:
        return False
    return model.objects.filter(user=request.user, recipe=obj).exists()
