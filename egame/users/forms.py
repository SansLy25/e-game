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
