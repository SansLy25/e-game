from typing import Any, Iterable, Optional

import django
from django import forms
from django.contrib.auth.forms import UserCreationForm
import django.forms

from practice.models import Exam
from users.models import User

__all__ = ()


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FormContext(dict):
    def __init__(
        self,
        forms: Iterable[django.forms.Form | django.forms.ModelForm],
        title: str,
        info: Optional[str] = None,
        description: Optional[str] = None,
        submit_button: str = "Отправить",
        reset_button: str = "Очистить",
        info_icon: Optional[str] = None,
        description_icon: Optional[str] = None,
        submit_button_icon: str = "bi-send",
        reset_button_icon: str = "bi-arrow-counterclockwise",
        reset_button_url: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(
            forms=forms,
            title=title,
            info=info,
            description=description,
            submit_button=submit_button,
            reset_button=reset_button,
            info_icon=info_icon,
            description_icon=description_icon,
            submit_button_icon=submit_button_icon,
            reset_button_icon=reset_button_icon,
            reset_button_url=reset_button_url,
            **kwargs,
        )


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    exams = forms.ModelMultipleChoiceField(
        queryset=Exam.objects.all(),
        required=True,
        label="Выберите экзамены",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("exams",)


class CustomAuthenticationForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.AuthenticationForm,
):
    pass


class UserSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
                " focus:outline-none focus:ring-2 focus:ring-blue-500"
                " dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                "placeholder": "Поиск по логину...",
            },
        ),
    )
