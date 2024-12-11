import django


class AnswerForm(django.forms.Form):
    selected_answer = django.forms.ChoiceField(
        widget=django.forms.RadioSelect,
        choices=[],
        label="Выберите ответ",
    )

    def __init__(self, *args, task=None, **kwargs):
        super().__init__(*args, **kwargs)
        if task:
            self.fields["selected_answer"].choices = [
                (option, option) for option in task.options
            ]


__all__ = AnswerForm
