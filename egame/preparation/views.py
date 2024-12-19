import django.contrib.auth.mixins
import django.http
import django.shortcuts
import django.urls
import django.views
import django.views.generic

import practice.models
import preparation.models


class BaseLoginRequired(django.contrib.auth.mixins.LoginRequiredMixin):
    login_url = "/"
    redirect_field_name = None


class TestListView(BaseLoginRequired, django.views.View):
    def get(self, request, exam_slug):
        exam = django.shortcuts.get_object_or_404(
            practice.models.Exam,
            slug=exam_slug,
        )
        tests = exam.tests.all()

        return django.shortcuts.render(
            request,
            "preparation/test_list.html",
            {"exam": exam, "tests": tests},
        )


class TaskView(BaseLoginRequired, django.views.View):
    def get(self, request, exam_slug, test_order):
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            order=test_order,
            exam__slug=exam_slug,
        )
        task = test.tasks.first()

        if task:
            return django.http.HttpResponseRedirect(
                django.urls.reverse(
                    "preparation:task_detail",
                    args=[exam_slug, test.order, task.order],
                ),
            )

        return django.shortcuts.render(
            request,
            "preparation/no_tasks.html",
            {"test": test},
        )


class TaskDetailView(BaseLoginRequired, django.views.View):
    def get(self, request, exam_slug, test_order, task_order):
        exam = django.shortcuts.get_object_or_404(
            practice.models.Exam,
            slug=exam_slug,
        )
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            order=test_order,
            exam=exam,
        )
        task = django.shortcuts.get_object_or_404(
            preparation.models.Task,
            order=task_order,
            test=test,
        )

        return django.shortcuts.render(
            request,
            "preparation/task_detail.html",
            {
                "test": test,
                "task": task,
                "options": task.get_shuffled_options(),
            },
        )

    def post(self, request, exam_slug, test_order, task_order):
        exam = django.shortcuts.get_object_or_404(
            practice.models.Exam,
            slug=exam_slug,
        )
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            order=test_order,
            exam=exam,
        )
        task = django.shortcuts.get_object_or_404(
            preparation.models.Task,
            order=task_order,
            test=test,
        )
        user_answer = request.POST.get("answer")

        session_key = f"test_{test.exam.slug}_{test.order}_answers"
        answers = request.session.get(session_key, {})
        answers[str(task.order)] = {
            "question": task.question,
            "user_answer": user_answer,
            "correct_answer": task.correct_answer,
        }
        request.session[session_key] = answers

        next_task = test.tasks.filter(order__gt=task.order).first()
        if next_task:
            return django.http.HttpResponseRedirect(
                django.urls.reverse(
                    "preparation:task_detail",
                    args=[exam_slug, test_order, next_task.order],
                ),
            )

        return django.http.HttpResponseRedirect(
            django.urls.reverse(
                "preparation:test_result",
                args=[exam_slug, test_order],
            ),
        )


class TestResultView(BaseLoginRequired, django.views.View):
    def get(self, request, exam_slug, order):
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            order=order,
            exam__slug=exam_slug,
        )

        session_key = f"test_{test.exam.slug}_{test.order}_answers"
        answers = request.session.get(session_key, {})

        return django.shortcuts.render(
            request,
            "preparation/test_result.html",
            {"test": test, "answers": answers},
        )
