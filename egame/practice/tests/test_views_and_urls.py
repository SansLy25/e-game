from django.test import TestCase
from django.utils.timezone import now, timedelta
from rest_framework import status
from rest_framework.test import APITestCase

from practice.models import Exam, Subtopic, Task, Theme, Variant


class VariantCreationViewTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(name="Sample Exam", slug="sample-exam")
        self.theme = Theme.objects.create(
            name="Sample Theme",
            task_number=1,
            exam=self.exam,
            is_answered=True,
        )
        self.subtopic = Subtopic.objects.create(
            name="Sample Subtopic",
            number=1,
            theme=self.theme,
        )
        self.task = Task.objects.create(
            subtopic=self.subtopic,
            task_text_html="<p>Sample Task</p>",
            task_solution_html="<p>Sample Solution</p>",
        )
        self.exam.save()

        self.url = f"{self.exam.slug}/practice/"

    def test_get_variant_creation_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_post_create_variant(self):
        form_data = {
            "expiration_time": 30,
            "1-counter": 1,
            "1-theme_id": self.theme.id,
            "1-subtopic": self.subtopic.id,
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VariantSolutionViewTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(name="Sample Exam", slug="sample-exam")
        self.theme = Theme.objects.create(
            name="Sample Theme",
            task_number=1,
            exam=self.exam,
            is_answered=True,
        )
        self.subtopic = Subtopic.objects.create(
            name="Sample Subtopic",
            number=1,
            theme=self.theme,
        )
        self.task = Task.objects.create(
            subtopic=self.subtopic,
            task_text_html="<p>Sample Task</p>",
            task_solution_html="<p>Sample Solution</p>",
        )
        self.variant = Variant.objects.create(
            expiration_time=now() + timedelta(days=1),
        )
        self.variant.tasks.add(self.task)
        self.url = f"/practice/{self.exam.slug}/{self.variant.id}/"

    def test_get_variant_solution_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSolutionAPITests(APITestCase):
    def setUp(self):
        self.exam = Exam.objects.create(name="Sample Exam", slug="sample-exam")
        self.theme = Theme.objects.create(
            name="Sample Theme",
            task_number=1,
            exam=self.exam,
            is_answered=True,
        )
        self.subtopic = Subtopic.objects.create(
            name="Sample Subtopic",
            number=1,
            theme=self.theme,
        )
        self.task = Task.objects.create(
            subtopic=self.subtopic,
            task_text_html="<p>Sample Task</p>",
            task_solution_html="<p>Sample Solution</p>",
        )
        self.variant = Variant.objects.create(
            expiration_time=now() + timedelta(days=1),
        )
        self.variant.tasks.add(self.task)
        self.variant.save()
        self.url = (
            f"/api/practice/get_solution/{self.variant.id}/{self.task.id}/",
        )

    def test_get_solution_invalid_variant(self):
        invalid_url = f"api/practice/get_solution/999/{self.task.id}/"
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_solution_task_not_in_variant(self):
        another_task = Task.objects.create(
            subtopic=self.subtopic,
            task_text_html="<p>Another Task</p>",
            task_solution_html="<p>Another Solution</p>",
        )
        invalid_url = (
            f"api/practice/get_solution/{self.variant.id}/{another_task.id}/",
        )
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
