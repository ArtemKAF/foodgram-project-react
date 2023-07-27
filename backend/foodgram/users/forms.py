"""Модуль создания, настройки и управления формами для ввода данных.

Описывает классы форм для создания и изменения пользователя. Классы форм
унаследованы от соответствующих форм Djando.
"""
from django.contrib.auth import forms, get_user_model
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(forms.UserChangeForm):
    """Класс формы для редактирования данных пользователя.
    """

    class Meta(forms.UserChangeForm.Meta):
        model = User
        field_classes = {'email': EmailField}


class UserAdminCreationForm(forms.UserCreationForm):
    """Класс формы для создания нового пользователя.
    """

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('email', )
        field_classes = {'email': EmailField}
        error_messages = {
            'email': {'unique': _('This email alredy been taken.')},
        }
