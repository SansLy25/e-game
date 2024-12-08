from django.test import Client, TestCase
from django.urls import reverse

from practice.models import Exam
from users.models import User

__all__ = ()


class SignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(name="Test Exam")
        cls.signup_url = reverse("users:signup")
        cls.profile_url = reverse("users:profile")

    def test_signup_page_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_page_template(self):
        response = self.client.get(self.signup_url)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_successful_signup(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "testuser",
                "password1": "testpass123",
                "password2": "testpass123",
                "exams": [self.exam.id],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], self.profile_url)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertTrue(
            User.objects.filter(username="testuser").exists(),
        )

    def test_invalid_signup(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "testuser",
                "password1": "testpass123",
                "password2": "wrongpass",
                "exams": [self.exam.id],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="testuser").exists(),
        )

    def test_signup_creates_user_with_exams(self):
        self.client.post(
            self.signup_url,
            {
                "username": "testuser",
                "password1": "testpass123",
                "password2": "testpass123",
                "exams": [self.exam.id],
            },
        )
        user = User.objects.get(username="testuser")
        self.assertIn(self.exam, user.exams.all())


class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(name="Test Exam")
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.user.exams.set([cls.exam])
        cls.login_url = reverse("users:login")
        cls.profile_url = reverse("users:profile")

    def test_login_page_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_page_template(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, "users/login.html")

    def test_successful_login(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )
        self.assertRedirects(response, self.profile_url)

    def test_invalid_login(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "wrongpass",
            },
        )
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(name="Test Exam")
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.friend = User.objects.create_user(
            username="frienduser",
            password="testpass123",
        )
        cls.user.exams.set([cls.exam])
        cls.profile_url = reverse("users:profile")

    def setUp(self):
        self.client = Client()

    def test_profile_requires_login(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(
            response,
            f"/login/?next={self.profile_url}",
        )

    def test_profile_accessible_when_logged_in(self):
        self.client.login(
            username="testuser",
            password="testpass123",
        )
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["user"],
            self.user,
        )

    def test_profile_shows_friends(self):
        self.client.login(
            username="testuser",
            password="testpass123",
        )
        self.user.friends.add(self.friend)
        response = self.client.get(self.profile_url)
        self.assertIn(self.friend, response.context["friends"])

    def test_profile_template(self):
        self.client.login(
            username="testuser",
            password="testpass123",
        )
        response = self.client.get(self.profile_url)
        self.assertTemplateUsed(response, "users/profile.html")
