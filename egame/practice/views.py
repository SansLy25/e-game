from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView

from practice.forms import TaskForm
from practice.models import Exam, Theme

__all__ = ["Theme", "Exam"]


class VariantCreationView(TemplateView):
    template_name = "practice/creation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = get_object_or_404(Exam, name=self.kwargs["exam_name"])
        themes_with_short_answer = Theme.objects.filter(
            exam=exam,
            is_answered=True,
        ).order_by("task_number")

        themes_with_long_answer = Theme.objects.filter(
            exam=exam,
            is_answered=False,
        ).order_by("task_number")
        forms = {}

        for theme in themes_with_short_answer | themes_with_long_answer:
            form = TaskForm(prefix=theme.task_number)
            form.fields["subtopic"].choices = [(0, "Случайная")] + [
                (subtopic.id, subtopic.name)
                for subtopic in theme.subtopics.all()
            ]
            form.fields["theme_id"].initial = str(theme.id)

            forms[f"form_{theme.id}"] = form

        context["themes_with_short_answer"] = themes_with_short_answer
        context["themes_with_long_answer"] = themes_with_long_answer
        context["forms"] = forms
        return context


class VariantSolutionView(FormView):
    template_name = "practice/solution.html"
