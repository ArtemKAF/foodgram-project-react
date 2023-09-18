"""Модуль вспомогательных функций для приложения рецептов.

Описывает различные вспомогательные функции для использования в приложении
рецептов.
"""
from collections import Counter

from django.utils.translation import gettext as _
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status
from rest_framework.response import Response


def generate_shopping_list_in_pdf(
        ingredients, filename, FONT_NAME, FONT_FILE, HEADER_FONT_SIZE,
        FONT_SIZE_IN_PT, TEXT_FONT_SIZE, LINE_SPACING, INDENTATION_HEADER,
        PAGE_SIZE, TOP_BORDER, HEADER_SPACING, INDENTATION_LIST, BOTTOM_BORDER,
):
    try:
        registerFont(TTFont(FONT_NAME, FONT_FILE, 'utf-8'))
    except Exception as e:
        return Response(
            {'errors': e.args},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    heading_height = HEADER_FONT_SIZE * FONT_SIZE_IN_PT
    text_height = TEXT_FONT_SIZE * FONT_SIZE_IN_PT
    line_spacing = LINE_SPACING * FONT_SIZE_IN_PT
    page = Canvas(filename=filename, pagesize=PAGE_SIZE)
    page.setFont(FONT_NAME, HEADER_FONT_SIZE)
    page.drawString(
        x=INDENTATION_HEADER,
        y=PAGE_SIZE[1] - TOP_BORDER - heading_height,
        text=_('Shopping list:'),
    )
    page.setFont(FONT_NAME, TEXT_FONT_SIZE)
    height = (
        PAGE_SIZE[1] - TOP_BORDER - heading_height - HEADER_SPACING
        - text_height
    )
    for ingredient in ingredients:
        page.drawString(
            INDENTATION_LIST,
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
        if height <= BOTTOM_BORDER:
            page.showPage()
            page.setFont(FONT_NAME, TEXT_FONT_SIZE)
            height = (PAGE_SIZE[1] - text_height - TOP_BORDER)
    page.save()


def is_in_something(serializer, model, obj, *args, **kwargs):
    request = serializer.context.get('request')
    if request is None or not request.user.is_authenticated:
        return False
    return model.objects.filter(user=request.user, recipe=obj).exists()


def create_delete_object(request, model, object, ser, err, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        if model.objects.filter(recipe=object, user=user).exists():
            return Response(
                {'errors': err},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(recipe=object, user=user)
        serializer = ser(object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    model.objects.filter(recipe=object, user=user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def validate_unique_items(items, item_name):
    count_items = Counter()
    for item in items:
        count_items[item[item_name]] += 1
    if len(count_items) != len(items):
        return [item.name for item in count_items if count_items[item] > 1]
