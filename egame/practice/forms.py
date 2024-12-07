from django import forms

__all__ = ["forms"]


class TaskForm(forms.Form):
    theme_id = forms.IntegerField(widget=forms.HiddenInput())

    counter = forms.IntegerField(
        min_value=1,
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
