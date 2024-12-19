from django.test import TestCase
from django.utils.timezone import now, timedelta
from practice.models import (
    Exam,
    Theme,
    Subtopic,
    Task,
    Answer,
    Variant,
    Solution,
    Fine,
)


class ModelsCRUDTestCase(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(
            name="Sample Exam",
            slug="sample-exam",
        )
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
        self.answer = Answer.objects.create(
            answer="Sample Answer",
            task=self.task,
        )
        self.variant = Variant.objects.create(
            expiration_time=now() + timedelta(days=1),
        )
        self.solution = Solution.objects.create(
            exam=self.exam,
            max_score=100,
            score=90,
            duration=timedelta(minutes=45),
            full_variant=True,
        )
        self.fine = Fine.objects.create(variant=self.variant, task=self.task)

    def test_create_objects(self):
        self.assertEqual(Exam.objects.count(), 1)
        self.assertEqual(Theme.objects.count(), 1)
        self.assertEqual(Subtopic.objects.count(), 1)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Variant.objects.count(), 1)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(Fine.objects.count(), 1)

    def test_delete_objects(self):
        self.exam.delete()
        self.assertEqual(Exam.objects.count(), 0)
        self.assertEqual(Theme.objects.count(), 0)
        self.assertEqual(Subtopic.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)

        self.variant.delete()
        self.assertEqual(Variant.objects.count(), 0)
        self.assertEqual(Fine.objects.count(), 0)

    def test_related_objects(self):
        self.assertEqual(self.theme.exam, self.exam)
        self.assertEqual(self.subtopic.theme, self.theme)
        self.assertEqual(self.task.subtopic, self.subtopic)
        self.assertEqual(self.answer.task, self.task)
        self.variant.tasks.add(self.task)
        self.assertIn(self.task, self.variant.tasks.all())

    def test_update_objects(self):
        self.exam.name = "Updated Exam"
        self.exam.save()
        updated_exam = Exam.objects.get(id=self.exam.id)
        self.assertEqual(updated_exam.name, "Updated Exam")

        self.solution.score = 95
        self.solution.save()
        updated_solution = Solution.objects.get(id=self.solution.id)
        self.assertEqual(updated_solution.score, 95)

    def test_cascade_deletion(self):
        self.theme.delete()
        self.assertEqual(Subtopic.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)

    def test_variant_tasks(self):
        new_task = Task.objects.create(
            subtopic=self.subtopic,
            task_text_html="<p>Another Task</p>",
            task_solution_html="<p>Another Solution</p>",
        )
        self.variant.tasks.add(new_task)
        self.assertIn(new_task, self.variant.tasks.all())
        self.variant.tasks.remove(new_task)
        self.assertNotIn(new_task, self.variant.tasks.all())
