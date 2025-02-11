from django import forms


class TaskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices", [])
        super().__init__(*args, **kwargs)
        self.fields["subtopic"].choices = choices

    theme_id = forms.IntegerField(widget=forms.HiddenInput())

    counter = forms.IntegerField(
        min_value=0,
        max_value=30,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "readonly": "readonly",
                "class": "w-6 text-center text-gray-900 "
                "dark:text-white border-none "
                "bg-transparent text-lg outline-none ",
                "style": "margin-left: 12px; width: 38px;",
            },
        ),
    )

    subtopic = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "text-xs w-full bg-white dark:bg-gray-800 "
                "border border-gray-300 dark:border-gray-600 "
                "rounded-lg py-2 px-3 text-gray-700 ml-10px "
                "dark:text-gray-300 appearance-none",
            },
        ),
    )


class AnswerForm(forms.Form):
    answer = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 bg-gray-700 border"
                " border-gray-600 rounded-md text-gray-100"
                " placeholder-gray-400 focus:ring-2"
                " focus:ring-blue-500 focus:border-transparent",
                "placeholder": "Введите свой ответ...",
            },
        ),
    )


class SolutionTimeForm(forms.Form):
    expiration_time = forms.IntegerField(
        min_value=10,
        max_value=320,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "id": "time-slider",
                "name": "time",
                "step": "1",
                "value": "185",
                "class": "w-full",
            },
        ),
    )
