from django.db import models


class DayOfWeek(models.Model):
    DAY_CHOICES = [
        (0, "Понедельник"),
        (1, "Вторник"),
        (2, "Среда"),
        (3, "Четверг"),
        (4, "Пятница"),
        (5, "Суббота"),
        (6, "Воскресенье"),
    ]

    day = models.IntegerField(choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return dict(self.DAY_CHOICES)[self.day]


class VisitedDay(models.Model):
    day = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="visited_days",
    )
