from django.utils.translation import gettext as _
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status
from rest_framework.response import Response


def generate_shopping_list_in_pdf(ingredients, filename):
        try:
            registerFont(
                TTFont('DejaVuSans', './data/DejaVuSans.ttf', 'utf-8')
            )
        except Exception as e:
            return Response(
                {'errors': e.args},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        page = Canvas(filename=filename)
        page.setFont('DejaVuSans', 20)
        page.drawString(230, 790, _('Shopping list:'))
        page.setFont('DejaVuSans', 12)
        height = 760
        for ingredient in ingredients:
            page.drawString(60, height, text=(
                '- {ingredient} ({measurement_unit}) -- {amount}'.format(
                    ingredient=ingredient.get('ingredient__name').capitalize(),
                    measurement_unit=ingredient.get(
                        'ingredient__measurement_unit'
                    ),
                    amount=ingredient.get('amount__sum'),
                )
            ))
            height -= 20
            if height <= 30:
                page.showPage()
                page.setFont('DejaVuSans', 12)
                height = 800
        page.save()
