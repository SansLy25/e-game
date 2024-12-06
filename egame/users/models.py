from django.contrib.auth.models import AbstractUser
from django.db import models

from practice.models import Exam

__all__ = ()


class User(AbstractUser):
    exams = models.ManyToManyField(
        Exam,
        blank=True,
        verbose_name="выбранные экзамены",
        related_name="users",
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username[:15]
