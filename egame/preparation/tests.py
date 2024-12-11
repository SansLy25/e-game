from django.test import TestCase
from django.urls import resolve, reverse

from preparation.models import Exam, Task, UserAnswer
from preparation.views import PreparationListView, TaskDetailView
from users.models import User


class TestPreparationUrls(TestCase):
    def test_exam_tasks_url(self):
        url = reverse("preparation:exam_tasks", kwargs={"exam": "math"})
        self.assertEqual(resolve(url).func.view_class, PreparationListView)

    def test_task_detail_url(self):
        url = reverse(
            "preparation:task_detail",
            kwargs={"exam": "math", "pk": 1},
        )
        self.assertEqual(resolve(url).func.view_class, TaskDetailView)


class TestPreparationViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        cls.exam = Exam.objects.create(name="math")
        cls.task = Task.objects.create(
            exam=cls.exam,
            question="Выберите правильную формулу дискриминанта",
            correct_answer="b^2 - 4ac",
            options=["b^2 - 4ac", "2b - 4a", "abc"],
        )

    def setUp(self):
        self.client.login(username="testuser", password="password")

    def test_preparation_list_view(self):
        url = reverse("preparation:exam_tasks", kwargs={"exam": "math"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "preparation/exam_tasks.html")
        self.assertIn(self.task, response.context["tasks"])

    def test_task_detail_view_get(self):
        url = reverse(
            "preparation:task_detail",
            kwargs={"exam": "math", "pk": self.task.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "preparation/task_detail.html")
        self.assertEqual(response.context["task"], self.task)

    def test_task_detail_view_post(self):
        url = reverse(
            "preparation:task_detail",
            kwargs={"exam": "math", "pk": self.task.pk},
        )
        data = {"selected_answer": "b^2 - 4ac"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

        user_answer = UserAnswer.objects.get(user=self.user, task=self.task)
        self.assertEqual(user_answer.selected_answer, "b^2 - 4ac")
        self.assertTrue(user_answer.is_correct)

    def test_redirect_if_not_authenticated(self):
        self.client.logout()

        list_url = reverse("preparation:exam_tasks", kwargs={"exam": "math"})
        detail_url = reverse(
            "preparation:task_detail",
            kwargs={"exam": "math", "pk": self.task.pk},
        )

        response = self.client.get(list_url)
        self.assertRedirects(response, "/")

        response = self.client.get(detail_url)
        self.assertRedirects(response, "/")


__all__ = ()
