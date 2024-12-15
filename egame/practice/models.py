from django.db import models


class Exam(models.Model):
    name = models.CharField("название", max_length=50)
    slug = models.SlugField("слаг", unique=True)

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

    is_answered = models.BooleanField(
        "из развернутой части",
        help_text="есть ли четкий ответ на задание",
    )

    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"

    def get_form_key(self):  # метод нужен для шаблона, вызвать str там нельзя
        return "form_" + str(self.id)

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
    subtopic = models.ForeignKey(
        Subtopic,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    task_text_html = models.TextField("текст задания")
    task_solution_html = models.TextField("текст решения")

    class Meta:
        verbose_name = "задание"
        verbose_name_plural = "задания"

    def get_form_key(self):  # метод нужен для шаблона, вызвать str там нельзя
        return "form_" + str(self.id)


class Answer(models.Model):
    answer = models.CharField("текст ответа", max_length=40)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"

    def __str__(self):
        return self.answer[:100]


class Variant(models.Model):
    expiration_time = models.DateTimeField("время окончания")
    date_created = models.DateTimeField("время создания", auto_now_add=True)
    tasks = models.ManyToManyField(Task, blank=True, verbose_name="задания")

    class Meta:
        verbose_name = "вариант"
        verbose_name_plural = "варианты"


class Solution(models.Model):
    date = models.DateField(
        "дата создания",
        auto_now_add=True,
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        verbose_name="экзамен",
    )

    max_score = models.PositiveIntegerField("максимальный балл")
    score = models.PositiveIntegerField("набранный балл")
    duration = models.DurationField("время решения")

    full_variant = models.BooleanField(
        "полный вариант",
        default=False,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="пользователь",
        related_name="solutions",
    )

    def get_score_percent(self):
        return round((self.score / self.max_score) * 100, 0)

    class Meta:
        verbose_name = "решение"
        verbose_name_plural = "решения"


class Fine(models.Model):
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        verbose_name="вариант",
        related_name="fines",
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="задание",
    )
