import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views.generic

import preparation.forms
import preparation.models


class BaseLoginRequired(django.contrib.auth.mixins.LoginRequiredMixin):
    login_url = "/"
    redirect_field_name = None


class PreparationListView(BaseLoginRequired, django.views.generic.ListView):
    template_name = "preparation/exam_tasks.html"
    context_object_name = "tasks"
    title = "Задания на запоминания"

    def get_queryset(self):
        exam = django.shortcuts.get_object_or_404(
            preparation.models.Exam,
            name=self.kwargs["exam"],
        )

        return preparation.models.Task.objects.filter(
            exam=exam,
        ).select_related("exam")


class TaskDetailView(
    BaseLoginRequired,
    django.views.generic.FormView,
    django.views.generic.DetailView,
):
    model = preparation.models.Task
    template_name = "preparation/task_detail.html"
    context_object_name = "task"
    form_class = preparation.forms.AnswerForm

    def get_object(self):
        if not hasattr(self, "_object"):
            self._object = django.shortcuts.get_object_or_404(
                preparation.models.Task,
                pk=self.kwargs["pk"],
            )

        return self._object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["task"] = self.get_object()

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_object()

        task = self.get_object()
        user_answers_queryset = task.user_answers.filter(
            user=self.request.user,
        )
        latest_user_answers = user_answers_queryset.order_by("-created_at")[:1]
        context["user_answers"] = latest_user_answers

        return context

    def form_valid(self, form):
        task = self.get_object()
        selected_answer = form.cleaned_data["selected_answer"]
        is_correct = selected_answer == task.correct_answer
        preparation.models.UserAnswer.objects.filter(
            task=task,
            user=self.request.user,
        ).delete()
        preparation.models.UserAnswer.objects.create(
            task=task,
            user=self.request.user,
            selected_answer=selected_answer,
            is_correct=is_correct,
        )

        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse(
            "preparation:task_detail",
            kwargs={
                "exam": self.get_object().exam.name,
                "pk": self.get_object().pk,
            },
        )


__all__ = (
    BaseLoginRequired,
    PreparationListView,
    TaskDetailView,
)
