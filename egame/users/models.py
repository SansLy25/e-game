from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from practice.models import Exam

__all__ = ()


class User(AbstractUser):
    exams = models.ManyToManyField(
        Exam,
        blank=True,
        verbose_name="выбранные экзамены",
        related_name="users",
    )
    friends = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=True,
        verbose_name="друзья",
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username[:15]

    def get_friend_link(self):
        return reverse("users:friends:add_by_username", args=[self.username])
