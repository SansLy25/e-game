import django.db.models


class Exam(django.db.models.Model):
    name = django.db.models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(django.db.models.Model):
    exam = django.db.models.ForeignKey(
        Exam,
        related_name="tasks",
        on_delete=django.db.models.CASCADE,
    )
    question = django.db.models.TextField()
    correct_answer = django.db.models.CharField(max_length=255)
    options = django.db.models.JSONField(
        help_text="Список вариантов ответа (JSON формат)",
    )

    def __str__(self):
        return self.question


class UserAnswer(django.db.models.Model):
    task = django.db.models.ForeignKey(
        Task,
        related_name="user_answers",
        on_delete=django.db.models.CASCADE,
    )
    user = django.db.models.ForeignKey(
        "users.User",
        on_delete=django.db.models.CASCADE,
    )
    selected_answer = django.db.models.CharField(max_length=255)
    is_correct = django.db.models.BooleanField(default=False)
    created_at = django.db.models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return (
            f"{self.user} - {self.task} - {self.selected_answer}"
            f" - {self.is_correct}"
        )


__all__ = (Exam, Task, UserAnswer)
