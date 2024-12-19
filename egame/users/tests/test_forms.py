import django.forms
import django.test

import users.forms
import users.models


class BootstrapFormMixinTest(django.test.TestCase):
    def test_bootstrap_form_mixin(self):
        class TestForm(django.forms.Form):
            field1 = django.forms.CharField()
            field2 = django.forms.EmailField()

        mixin_form = TestForm()
        mixin_form.__class__ = type(
            "TestFormWithMixin",
            (users.forms.BootstrapFormMixin, TestForm),
            {},
        )
        mixin_form.__init__()

        for field in mixin_form.visible_fields():
            self.assertIn("class", field.field.widget.attrs)
            self.assertEqual(field.field.widget.attrs["class"], "form-control")


class CustomUserCreationFormTest(django.test.TestCase):
    def setUp(self):
        users.models.DayOfWeek.objects.create(day=0)
        users.models.Exam.objects.create(name="Math")

    def tearDown(self):
        users.models.Exam.objects.all().delete()
        users.models.DayOfWeek.objects.all().delete()

        super(CustomUserCreationFormTest, self).tearDown()

    def test_valid_data(self):
        day_of_week_id = users.models.DayOfWeek.objects.first().id
        exam_id = users.models.Exam.objects.first().id

        data = {
            "username": "testuser",
            "password1": "securepassword",
            "password2": "securepassword",
            "days_of_lessons": [day_of_week_id],
            "exams": [exam_id],
        }
        form = users.forms.CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_missing_days_of_lessons(self):
        exam_id = users.models.Exam.objects.first().id

        data = {
            "username": "testuser",
            "password1": "securepassword",
            "password2": "securepassword",
            "exams": [exam_id],
        }
        form = users.forms.CustomUserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("days_of_lessons", form.errors)

    def test_missing_exams(self):
        day_of_week_id = users.models.DayOfWeek.objects.first().id

        data = {
            "username": "testuser",
            "password1": "securepassword",
            "password2": "securepassword",
            "days_of_lessons": [day_of_week_id],
        }
        form = users.forms.CustomUserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("exams", form.errors)


class CustomAuthenticationFormTest(django.test.TestCase):
    def setUp(self):
        self.user = users.models.User.objects.create_user(
            username="testuser",
            password="password",
        )

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(CustomAuthenticationFormTest, self).tearDown()

    def test_valid_credentials(self):
        data = {
            "username": "testuser",
            "password": "password",
        }
        form = users.forms.CustomAuthenticationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_credentials(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        form = users.forms.CustomAuthenticationForm(data=data)
        self.assertFalse(form.is_valid())


class UserSearchFormTest(django.test.TestCase):
    def test_valid_data(self):
        data = {"username": "testuser"}
        form = users.forms.UserSearchForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_empty_data(self):
        data = {}
        form = users.forms.UserSearchForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")
