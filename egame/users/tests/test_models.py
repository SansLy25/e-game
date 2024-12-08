from django.test import TestCase

from practice.models import Exam
from users.models import User

__all__ = ()


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(name="Test Exam")
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.user.exams.set([cls.exam])

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "testuser")

    def test_user_exam_relationship(self):
        self.assertEqual(self.user.exams.last(), self.exam)

    def test_user_verbose_names(self):
        self.assertEqual(
            User._meta.verbose_name,
            "пользователь",
        )
        self.assertEqual(
            User._meta.verbose_name_plural,
            "пользователи",
        )

    def test_exam_can_be_null(self):
        user = User.objects.create_user(
            username="testuser2",
            password="testpass123",
        )
        self.assertFalse(user.exams.exists())
