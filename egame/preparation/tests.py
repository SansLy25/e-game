import http

import django.shortcuts
import django.test
import django.urls

import practice.models
import preparation.models
import users.models


class PreparationTests(django.test.TestCase):
    def setUp(self):
        self.exam = practice.models.Exam.objects.create(
            name="Математика",
            slug="math",
        )

        self.test = preparation.models.Test.objects.create(
            exam=self.exam,
            title="Свойства степеней",
        )

        self.task1 = preparation.models.Task.objects.create(
            test=self.test,
            question="Какова степень произведения \\(2^3 \\cdot 2^4\\?",
            correct_answer="\\(2^7\\)",
            options=["\\(2^5\\)", "\\(2^6\\)", "\\(2^7\\)", "\\(2^8\\)"],
            order=1,
        )
        self.task2 = preparation.models.Task.objects.create(
            test=self.test,
            question="Каково значение \\((3^2)^3\\)?",
            correct_answer="\\(3^6\\)",
            options=["\\(3^5\\)", "\\(3^6\\)", "\\(3^7\\)", "\\(3^8\\"],
            order=2,
        )

        self.user = users.models.User.objects.create_user(
            username="testuser",
            password="password",
        )

        self.client.login(username="testuser", password="password")

        super(PreparationTests, self).setUp()

    def tearDown(self):
        practice.models.Exam.objects.all().delete()
        preparation.models.Test.objects.all().delete()
        preparation.models.Task.objects.all().delete()
        users.models.User.objects.all().delete()

        super(PreparationTests, self).tearDown()

    def test_test_list_view(self):
        url = django.urls.reverse(
            "preparation:test_list",
            args=[self.exam.slug],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.test.title)

    def test_task_view_redirects_to_first_task(self):
        url = django.urls.reverse(
            "preparation:test",
            args=[self.exam.slug, self.test.id],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.urls.reverse(
                "preparation:task_detail",
                args=[self.exam.slug, self.test.id, self.task1.id],
            ),
        )

    def test_task_detail_view(self):
        url = django.urls.reverse(
            "preparation:task_detail",
            args=[self.exam.slug, self.test.id, self.task1.id],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.task1.question)

    def test_task_detail_post_next_task(self):
        url = django.urls.reverse(
            "preparation:task_detail",
            args=[self.exam.slug, self.test.id, self.task1.id],
        )
        response = self.client.post(url, {"answer": "\\(2^7\\)"})

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.urls.reverse(
                "preparation:task_detail",
                args=[self.exam.slug, self.test.id, self.task2.id],
            ),
        )

    def test_task_detail_post_result_redirect(self):
        self.client.post(
            django.urls.reverse(
                "preparation:task_detail",
                args=[self.exam.slug, self.test.id, self.task1.id],
            ),
            {"answer": "\\(2^7\\)"},
        )

        response = self.client.post(
            django.urls.reverse(
                "preparation:task_detail",
                args=[self.exam.slug, self.test.id, self.task2.id],
            ),
            {"answer": "\\(3^6\\)"},
        )

        result_url = django.urls.reverse(
            "preparation:test_result",
            args=[self.exam.slug, self.test.id],
        )

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, result_url)

    def test_test_result_view(self):
        """Тест отображения результатов"""
        # Заполняем ответы в сессии
        session = self.client.session
        session[f"test_{self.test.id}_answers"] = {
            str(self.task1.id): {
                "question": self.task1.question,
                "user_answer": "\\(2^7\\)",
                "correct_answer": self.task1.correct_answer,
            },
            str(self.task2.id): {
                "question": self.task2.question,
                "user_answer": "\\(3^6\\)",
                "correct_answer": self.task2.correct_answer,
            },
        }
        session.save()

        url = django.urls.reverse(
            "preparation:test_result",
            args=[self.exam.slug, self.test.id],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.task1.question)
        self.assertContains(response, "\\(2^7\\)")
        self.assertContains(response, self.task1.correct_answer)

    def test_redirect_if_not_authenticated(self):
        self.client.logout()

        list_url = django.urls.reverse(
            "preparation:test_list",
            kwargs={"exam_slug": "math"},
        )
        detail_url = django.urls.reverse(
            "preparation:test",
            kwargs={"exam_slug": "math", "order": self.task1.order},
        )

        response = self.client.get(list_url)
        self.assertRedirects(response, "/")

        response = self.client.get(detail_url)
        self.assertRedirects(response, "/")


__all__ = ()
