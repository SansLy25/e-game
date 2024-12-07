from django import template

__all__ = ["template"]

register = template.Library()


@register.simple_tag
def get_form_field(forms, form_key, field):
    """
    Возвращает поле формы по ключу из словаря forms.

    :param forms: словарь форм
    :param form_key: ключ для получения формы из словаря
    :param field: название поля формы
    :return: поле формы или None
    """
    try:
        form = forms.get(form_key)
        return form[field]
    except (AttributeError, KeyError):
        pass

    return None
