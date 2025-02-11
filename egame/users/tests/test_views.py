import http

import django.test
import django.urls

import practice.models
import users.models


class SignUpViewTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = practice.models.Exam.objects.create(name="Test Exam")
        cls.signup_url = django.urls.reverse("users:signup")
        cls.profile_url = django.urls.reverse("users:profile")
        cls.dayofweek = users.models.DayOfWeek.objects.create(day=0)

    def tearDown(self):
        practice.models.Exam.objects.all().delete()
        users.models.DayOfWeek.objects.all().delete()

        super(SignUpViewTest, self).tearDown()

    def test_signup_page_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_signup_page_template(self):
        response = self.client.get(self.signup_url)
        self.assertTemplateUsed(response, "users/auth.html")

    def test_successful_signup(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "testuser",
                "password1": "testpass123",
                "password2": "testpass123",
                "exams": [self.exam.id],
                "days_of_lessons": [self.dayofweek.id],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTrue(
            users.models.User.objects.filter(username="testuser").exists(),
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
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertFalse(
            users.models.User.objects.filter(username="testuser").exists(),
        )

    def test_signup_creates_user_with_exams(self):
        day_of_week_id = users.models.DayOfWeek.objects.first().id
        exam_id = users.models.Exam.objects.first().id

        data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "exams": [exam_id],
            "days_of_lessons": [day_of_week_id],
        }

        self.client.post(
            self.signup_url,
            data,
        )
        user = users.models.User.objects.get(username="testuser")
        self.assertIn(self.exam, user.exams.all())


class LoginViewTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = practice.models.Exam.objects.create(name="Test Exam")
        cls.user = users.models.User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.user.exams.set([cls.exam])
        cls.login_url = django.urls.reverse("users:login")
        cls.profile_url = django.urls.reverse("users:profile")

    def tearDown(self):
        practice.models.Exam.objects.all().delete()
        users.models.User.objects.all().delete()

        super(LoginViewTest, self).tearDown()

    def test_login_page_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_login_page_template(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, "users/auth.html")

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
        self.assertEqual(response.status_code, http.HTTPStatus.OK)


class ProfileViewTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = users.models.Exam.objects.create(name="Test Exam")
        cls.user = users.models.User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.friend = users.models.User.objects.create_user(
            username="frienduser",
            password="testpass123",
        )
        cls.user.exams.set([cls.exam])
        cls.profile_url = django.urls.reverse("users:profile")

    def tearDown(self):
        practice.models.Exam.objects.all().delete()
        users.models.User.objects.all().delete()

        super(ProfileViewTest, self).tearDown()

    def setUp(self):
        self.client = django.test.Client()

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
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
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
