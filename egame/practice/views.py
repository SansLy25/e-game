import datetime
import random

from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localtime
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from practice.forms import AnswerForm, SolutionTimeForm, TaskForm
from practice.models import (
    Exam,
    Fine,
    Solution,
    Subtopic,
    Task,
    Theme,
    Variant,
)

__all__ = [
    "Theme",
    "Exam",
    "Variant",
    "Subtopic",
    "TaskForm",
    "SolutionTimeForm",
    "localtime",
    "AnswerForm",
    "Task",
    "Fine",
]


class VariantCreationView(TemplateView):
    template_name = "practice/creation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = get_object_or_404(Exam, slug=self.kwargs["exam_slug"])
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
            choices = [(0, "Случайная")] + [
                (subtopic.id, subtopic.name)
                for subtopic in theme.subtopics.filter(
                    tasks__isnull=False,
                ).distinct()
            ]
            form = TaskForm(prefix=theme.task_number, choices=choices)

            form.fields["theme_id"].initial = str(theme.id)

            forms[f"form_{theme.id}"] = form

        context["themes_with_short_answer"] = themes_with_short_answer
        context["themes_with_long_answer"] = themes_with_long_answer
        context["forms"] = forms
        context["time_form"] = SolutionTimeForm()
        return context

    def post(self, request, *args, **kwargs):
        exam = get_object_or_404(Exam, slug=self.kwargs["exam_slug"])
        themes = Theme.objects.filter(exam=exam)
        time_form = SolutionTimeForm(request.POST)
        forms = []

        for theme in themes:
            choices = [(0, "Случайная")] + [
                (subtopic.id, subtopic.name)
                for subtopic in theme.subtopics.filter(
                    tasks__isnull=False,
                ).distinct()
            ]
            form = TaskForm(
                request.POST,
                prefix=theme.task_number,
                choices=choices,
            )
            forms.append(form)

        if all(form.is_valid() for form in forms) and time_form.is_valid():
            expiration_time = time_form.cleaned_data["expiration_time"]
            expiration_date_time = localtime() + datetime.timedelta(
                minutes=expiration_time,
            )

            variant = Variant(expiration_time=expiration_date_time)
            variant.save()

            for form in forms:
                if int(form.cleaned_data["subtopic"]) == 0:
                    theme = Theme.objects.get(id=form.cleaned_data["theme_id"])
                    subtopic = random.choice(
                        list(
                            Subtopic.objects.filter(
                                theme=theme,
                                tasks__isnull=False,
                            ).distinct(),
                        ),
                    )

                else:
                    subtopic = Subtopic.objects.get(
                        id=int(form.cleaned_data["subtopic"]),
                    )

                count = form.cleaned_data["counter"]
                count_available = subtopic.tasks.count()
                if count != 0:
                    tasks = random.sample(
                        list(subtopic.tasks.all()),
                        count if count <= count_available else count_available,
                    )
                    variant.tasks.add(*tasks)

            variant.save()
            return redirect(
                "variant_solution",
                exam_slug=exam.slug,
                variant_id=variant.id,
            )

        return render(
            request,
            self.template_name,
            self.get_context_data(forms=forms),
        )


class VariantSolutionView(TemplateView):
    template_name = "practice/solution.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_object_or_404(Exam, slug=self.kwargs["exam_slug"])
        variant = get_object_or_404(Variant, id=self.kwargs["variant_id"])
        context["variant"] = variant
        context["expiration_date"] = variant.date_created.strftime(
            "%Y-%m-%d %H:%M:%S",
        )  # для скрипта
        context["date_created"] = variant.expiration_time.strftime(
            "%Y-%m-%d %H:%M:%S",
        )

        forms = {}

        for task in variant.tasks.filter(subtopic__theme__is_answered=True):
            form = AnswerForm(prefix=task.id)
            forms[f"form_{task.id}"] = form

        context["forms"] = forms

        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = get_object_or_404(Exam, slug=self.kwargs["exam_slug"])
        variant = get_object_or_404(Variant, id=self.kwargs["variant_id"])
        tasks = []
        max_score, score = 0, 0

        for task in variant.tasks.filter(subtopic__theme__is_answered=True):
            form = AnswerForm(request.POST, prefix=task.id)
            if form.is_valid():
                task_answers = [answer.answer for answer in task.answers.all()]
                answer = form.cleaned_data["answer"]

                if answer in task_answers and answer != "":
                    if Fine.objects.filter(
                        task=task, variant=variant,
                    ).exists():
                        task_score = 0
                    else:
                        task_score = 1
                        score += 1
                else:
                    task_score = 0

                tasks.append(
                    {
                        "name": task.subtopic.theme.name,
                        "score": task_score,
                        "max_score": 1,
                    },
                )

                max_score += 1

        if (
            variant.tasks.filter(subtopic__theme__is_answered=True).count()
            == Theme.objects.filter(exam=exam, is_answered=True).count()
        ):
            full_variant = True
        else:
            full_variant = False

        duration = localtime() - localtime(variant.date_created)
        user = request.user if request.user.is_authenticated else None

        solution = Solution(
            date=localtime(),
            exam=exam,
            max_score=max_score,
            score=score,
            duration=duration,
            full_variant=full_variant,
            user=user,
        )
        solution.save()
        total_seconds = duration.total_seconds()

        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        formatted_time = f"{int(hours):02}:{int(minutes):02}"

        context["duration"] = formatted_time
        context["tasks"] = tasks
        context["percent"] = (
            round(100 * (score / max_score), 1) if max_score != 0 else 0
        )
        context["score"] = score
        context["max_score"] = max_score
        context["rating"] = int(
            self.linear_to_coefficient(total_seconds // 60) * 10 * score,
        )

        variant.delete()

        return render(request, "practice/result.html", context)

    @staticmethod  # метод для конвертации времени в коэффициент рейтинга
    def linear_to_coefficient(value):
        if value <= 10:
            return 4.0

        if value >= 320:
            return 0.4

        return 0.4 + (4.0 - 0.4) * (320 - value) / (320 - 10)


class GetSolutionAPIView(APIView):
    def get(self, request, variant_id, task_id):
        variant = get_object_or_404(Variant, id=variant_id)
        task = get_object_or_404(Task, id=task_id)

        if localtime(variant.expiration_time) < localtime():
            return Response(
                {"detail": "Вариант недействителен"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if task not in variant.tasks.all():
            return Response(
                {"detail": "Задание не находится в этом варианте"},
                status=status.HTTP_403_FORBIDDEN,
            )

        response = {
            "answers": [answer.answer for answer in task.answers.all()],
            "solution": task.task_solution_html,
        }

        if task.subtopic.theme.is_answered:
            fine = Fine(task=task, variant=variant)
            fine.save()

        return Response(response, status=status.HTTP_200_OK)
