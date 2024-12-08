from django.test import TestCase

from practice.models import Exam
from users.forms import CustomUserCreationForm

__all__ = ()


class CustomUserCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(name="Test Exam")

    def test_form_has_exam_field(self):
        form = CustomUserCreationForm()
        self.assertIn("exams", form.fields)

    def test_form_valid_data(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "password1": "testpass123",
                "password2": "testpass123",
                "exams": [self.exam.id],
            },
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_exam(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("exams", form.errors)

    def test_form_password_mismatch(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "password1": "testpass123",
                "password2": "wrongpass",
                "exams": [self.exam.id],
            },
        )
        self.assertFalse(form.is_valid())
