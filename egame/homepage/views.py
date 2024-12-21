import random

from django.shortcuts import redirect, render
from django.views.generic import TemplateView

PHRASES = {
    "physics": [
        "Сила тяжести — это сила, которая притягивает физиков к земле",
        "Электричество и магнетизм — это как "
        "две стороны одной медали, которые всегда вместе",
        "Теплопередача — это процесс, "
        "который помогает нам согреться зимой и охладиться летом",
        "Свет — это волна или частица?  А может быть, и то, и другое?",
    ],
    "math": [
        "Системы уравнений — это как головоломки,"
        " которые нужно решить, чтобы получить ответ",
        "Геометрические фигуры — это основа всего, что нас окружает",
        "Теория вероятностей — это наука о том,"
        " как предсказать будущее на основе прошлого",
        "Тригонометрия — это язык, на котором говорят углы",
    ],
    "russian": [
        "Стили речи — это как разные костюмы, "
        "которые мы надеваем в зависимости от ситуации",
        "Части речи — это инструменты, "
        "с помощью которых мы строим предложения",
        "Синтаксис — это правила, по которым строятся предложения",
        "Орфография — это свод законов,"
        " которые нужно соблюдать при написании слов",
    ],
}


class HomePageView(TemplateView):
    template_name = "homepage/getting_started.html"
    template_name_for_authed = "homepage/main.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("homepage:exam_home", exam_slug="math")

        return render(request, self.template_name)


class ExamHomePageView(TemplateView):
    template_name = "homepage/exam_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["exam_slug"] == "math":
            verbose = "Математикой"
        elif context["exam_slug"] == "russian":
            verbose = "Русским языком"
        elif context["exam_slug"] == "physics":
            verbose = "Физикой"
        else:
            verbose = ""

        context["verbose_exam"] = verbose
        context["phrase"] = random.choice(PHRASES[context["exam_slug"]])
        return context
