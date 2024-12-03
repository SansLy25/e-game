from django.db import models


class Exam(models.Model):
    name = models.CharField("название", max_length=50)

    class Meta:
        verbose_name = "экзамен"
        verbose_name_plural = "экзамены"

    def __str__(self):
        return self.name[:15]


class Theme(models.Model):
    name = models.CharField("тема", max_length=100)
    task_number = models.PositiveIntegerField("номер задания")
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        verbose_name="экзамен",
        related_name="themes",
    )

    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"

    def __str__(self):
        return self.name[:15]


class Subtopic(models.Model):
    name = models.CharField("подтема", max_length=100)
    number = models.PositiveIntegerField("номер подтемы")
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        verbose_name="тема",
        related_name="subtopics",
    )

    class Meta:
        verbose_name = "подтема"
        verbose_name_plural = "подтемы"

    def __str__(self):
        return self.name[:15]


class Task(models.Model):
    task_text_html = models.TextField("текст задания")
    task_solution_html = models.TextField("текст решения")
    is_answered = models.BooleanField(
        "из развернутой части",
        default=False,
        help_text="есть ли четкий ответ на задание",
    )

    class Meta:
        verbose_name = "задание"
        verbose_name_plural = "задания"


class Answer(models.Model):
    answer = models.CharField("текст ответа", max_length=40)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="answers"
    )

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"

    def __str__(self):
        return self.answer[:100]
