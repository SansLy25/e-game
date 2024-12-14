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
    def get(self, request, exam_slug, order):
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            pk=order,
            exam__slug=exam_slug,
        )
        task = test.tasks.first()

        if task:
            return django.http.HttpResponseRedirect(
                django.urls.reverse(
                    "preparation:task_detail",
                    args=[exam_slug, test.id, task.order],
                ),
            )

        return django.shortcuts.render(
            request,
            "preparation/no_tasks.html",
            {"test": test},
        )


class TaskDetailView(BaseLoginRequired, django.views.View):
    def get(self, request, exam_slug, test_id, order):
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            pk=test_id,
            exam__slug=exam_slug,
        )
        task = django.shortcuts.get_object_or_404(
            preparation.models.Task,
            order=order,
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

    def post(self, request, exam_slug, test_id, order):
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            pk=test_id,
            exam__slug=exam_slug,
        )
        task = django.shortcuts.get_object_or_404(
            preparation.models.Task,
            test=test,
            order=order,
        )
        user_answer = request.POST.get("answer")

        session_key = f"test_{test.id}_answers"
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
                    args=[exam_slug, test_id, next_task.order],
                ),
            )

        return django.http.HttpResponseRedirect(
            django.urls.reverse(
                "preparation:test_result",
                args=[exam_slug, test_id],
            ),
        )


class TestResultView(BaseLoginRequired, django.views.View):
    def get(self, request, exam_slug, test_id):
        test = django.shortcuts.get_object_or_404(
            preparation.models.Test,
            pk=test_id,
            exam__slug=exam_slug,
        )
        answers = request.session.get(f"test_{test.id}_answers", {})

        return django.shortcuts.render(
            request,
            "preparation/test_result.html",
            {"test": test, "answers": answers},
        )


__all__ = ()
