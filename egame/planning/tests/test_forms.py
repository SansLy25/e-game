import django.forms
import django.test

import planning.forms
import users.models


class LessonsDaysEditFormTests(django.test.TestCase):
    def setUp(self):
        self.user = users.models.User.objects.create(username="testuser")
        self.monday = users.models.DayOfWeek.objects.create(day=0)
        self.wednesday = users.models.DayOfWeek.objects.create(day=2)
        self.friday = users.models.DayOfWeek.objects.create(day=4)

        super(LessonsDaysEditFormTests, self).setUp()

    def tearDown(self):
        users.models.User.objects.all().delete()
        users.models.DayOfWeek.objects.all().delete()

        super(LessonsDaysEditFormTests, self).tearDown()

    def test_form_initialization_with_instance(self):
        self.user.days_of_lessons.set([self.monday, self.wednesday])

        form = planning.forms.LessonsDaysEditForm(instance=self.user)

        self.assertIn("days_of_lessons", form.initial)
        self.assertEqual(
            set(form.initial["days_of_lessons"]),
            set([self.monday, self.wednesday]),
        )

    def test_form_fields_configuration(self):
        form = planning.forms.LessonsDaysEditForm()

        self.assertIn("days_of_lessons", form.fields)
        self.assertIsInstance(
            form.fields["days_of_lessons"],
            django.forms.ModelMultipleChoiceField,
        )
        self.assertEqual(
            set(form.fields["days_of_lessons"].queryset),
            set(users.models.DayOfWeek.objects.all()),
        )
        self.assertEqual(
            form.fields["days_of_lessons"].label,
            "Дни недели для занятий",
        )

    def test_form_save(self):
        form_data = {
            "days_of_lessons": [self.monday.pk, self.friday.pk],
        }

        form = planning.forms.LessonsDaysEditForm(
            data=form_data,
            instance=self.user,
        )

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(
            set(self.user.days_of_lessons.all()),
            set([self.monday, self.friday]),
        )
