import django.db.models

import practice.models


class Test(django.db.models.Model):
    exam = django.db.models.ForeignKey(
        practice.models.Exam,
        on_delete=django.db.models.CASCADE,
        related_name="tests",
        verbose_name="экзамен",
    )
    title = django.db.models.CharField("заголовок", max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"


class Task(django.db.models.Model):
    test = django.db.models.ForeignKey(
        Test,
        on_delete=django.db.models.CASCADE,
        related_name="tasks",
        verbose_name="тест",
    )
    question = django.db.models.TextField("вопрос")
    correct_answer = django.db.models.CharField(
        "правильный ответ",
        max_length=255,
    )
    options = django.db.models.JSONField("варианты ответа")
    order = django.db.models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.test.title} - {self.question}"

    class Meta:
        unique_together = (
            "test",
            "order",
        )  # Уникальность порядка внутри одного теста
        ordering = ["order"]  # Задания автоматически сортируются по порядку
        verbose_name = "задание"
        verbose_name_plural = "задания"

    def get_shuffled_options(self):
        import random

        options = self.options.copy()
        random.shuffle(options)
        return options


__all__ = (Test, Task)
