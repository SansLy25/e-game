from dataclasses import dataclass
from typing import Any, Literal, Optional

from django import forms
from django.contrib.auth.forms import UserCreationForm
import django.forms
from django.views.generic import FormView

from planning.models import DayOfWeek
from practice.models import Exam
from users.models import User


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


@dataclass
class FormAdditions:
    text: Optional[str] = None
    icon: Optional[str] = None


@dataclass
class FormButton(FormAdditions):
    url: Optional[str] = None


@dataclass
class FormFooterItem(FormButton):
    link_text: Optional[str] = None


class FormContext(dict):
    def __init__(
        self,
        title: str,
        info: Optional[FormAdditions] = None,
        description: Optional[FormAdditions] = None,
        submit: Optional[FormButton | Literal[False]] = None,
        cancel: Optional[FormButton | Literal[False]] = None,
        *footer_items: FormFooterItem,
        **kwargs: Any,
    ):
        if submit is None:
            submit = FormButton()

        if submit:
            submit = FormButton(
                submit.text or "Отправить",
                submit.icon or "bi-send",
                submit.url,
            )

        if cancel is None:
            cancel = FormButton()

        if cancel:
            cancel = FormButton(
                cancel.text or "Отмена",
                cancel.icon or "bi-x-circle",
                cancel.url,
            )

        super().__init__(
            title=title,
            info=info,
            description=description,
            submit=submit,
            cancel=cancel,
            footer_items=footer_items,
            **kwargs,
        )

    def __call__(self, view: FormView, kwargs):
        self.setdefault("forms", [view.get_form()])
        self.update(kwargs)
        return self


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    days_of_lessons = forms.ModelMultipleChoiceField(
        queryset=DayOfWeek.objects.all(),
        required=True,
        label="Выберите дни недели для занятий",
        widget=forms.CheckboxSelectMultiple,
    )

    exams = forms.ModelMultipleChoiceField(
        queryset=Exam.objects.all(),
        required=True,
        label="Выберите экзамены",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("exams", "days_of_lessons")


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
                "class": "form-control",
                "placeholder": "Поиск",
            },
        ),
    )
