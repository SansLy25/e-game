from django import forms
from django.contrib.auth.forms import UserCreationForm

from practice.models import Exam
from users.models import User

__all__ = ()


class CustomUserCreationForm(UserCreationForm):
    exams = forms.ModelMultipleChoiceField(
        queryset=Exam.objects.all(),
        required=True,
        label="Выберите экзамены",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("exams",)


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
