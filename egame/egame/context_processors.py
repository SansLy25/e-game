import django.conf

__all__ = []


def navigation(request):
    return {"nav_items": django.conf.settings.NAVIGATION_ITEMS}
