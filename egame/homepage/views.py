from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "homepage/main.html"


__all__ = ()
