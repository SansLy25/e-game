import django.test
import django.forms

import practice.forms


class TaskFormTests(django.test.TestCase):
    def test_task_form_initialization_with_choices(self):
        choices = [(1, "Subtopic 1"), (2, "Subtopic 2")]
        form = practice.forms.TaskForm(choices=choices)
        self.assertEqual(form.fields["subtopic"].choices, choices)

    def test_task_form_theme_id_field(self):
        form = practice.forms.TaskForm()
        self.assertIn("theme_id", form.fields)
        self.assertIsInstance(
            form.fields["theme_id"].widget, django.forms.HiddenInput,
        )

    def test_task_form_counter_field(self):
        form = practice.forms.TaskForm()
        counter_field = form.fields["counter"]
        self.assertEqual(counter_field.min_value, 0)
        self.assertEqual(counter_field.max_value, 30)
        self.assertEqual(counter_field.initial, 1)
        self.assertIsInstance(counter_field.widget, django.forms.NumberInput)
        self.assertIn("readonly", counter_field.widget.attrs)

    def test_task_form_subtopic_field(self):
        form = practice.forms.TaskForm()
        subtopic_field = form.fields["subtopic"]
        self.assertIsInstance(subtopic_field.widget, django.forms.Select)
        self.assertIn("class", subtopic_field.widget.attrs)


class AnswerFormTests(django.test.TestCase):
    def test_answer_form_initialization(self):
        form = practice.forms.AnswerForm()
        self.assertIn("answer", form.fields)
        self.assertIsInstance(
            form.fields["answer"].widget, django.forms.TextInput,
        )
        self.assertIn("placeholder", form.fields["answer"].widget.attrs)
        self.assertEqual(
            form.fields["answer"].widget.attrs["placeholder"],
            "Введите свой ответ...",
        )


class SolutionTimeFormTests(django.test.TestCase):
    def test_solution_time_form_initialization(self):
        form = practice.forms.SolutionTimeForm()
        self.assertIn("expiration_time", form.fields)
        expiration_field = form.fields["expiration_time"]
        self.assertEqual(expiration_field.min_value, 10)
        self.assertEqual(expiration_field.max_value, 320)
        self.assertIsInstance(
            expiration_field.widget, django.forms.NumberInput,
        )
