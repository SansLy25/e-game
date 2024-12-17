import django.template

register = django.template.Library()


@register.filter
def get_field_icon(field):
    field_name = field.name.lower()
    field_type = (
        field.field.widget.input_type
        if hasattr(field.field.widget, "input_type")
        else ""
    )

    icon_mapping = {
        "name": "bi-person",
        "username": "bi-person",
        "email": "bi-envelope",
        "password": "bi-lock",
        "password1": "bi-lock",
        "password2": "bi-lock",
        "old_password": "bi-shield-lock",
        "new_password1": "bi-lock",
        "new_password2": "bi-lock",
        "first_name": "bi-person-vcard",
        "last_name": "bi-person-vcard",
        "phone": "bi-telephone",
        "subject": "bi-chat-left-text",
        "message": "bi-chat-text",
        "file": "bi-paperclip",
        "date": "bi-calendar",
        "time": "bi-clock",
        "datetime": "bi-calendar-date",
        "number": "bi-hash",
    }

    icon = icon_mapping.get(field_name)

    if icon is None and field_type:
        icon = icon_mapping.get(field_type)

    if icon is None:
        return None

    return icon
