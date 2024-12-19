from django import forms

from planning.models import DayOfWeek
from users.models import User


class LessonsDaysEditForm(forms.ModelForm):
    days_of_lessons = forms.ModelMultipleChoiceField(
        queryset=DayOfWeek.objects.all(),
        label="Дни недели для занятий",
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["days_of_lessons"] = (
                self.instance.days_of_lessons.all()
            )

    class Meta:
        model = User
        fields = ["days_of_lessons"]
