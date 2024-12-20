from django.db import models

from users.models import User


class AchievementManager(models.Manager):
    def by_slug(self, slug: str):
        return self.get(slug=slug)


class Achievement(models.Model):
    name = models.CharField("название", max_length=30)
    slug = models.SlugField("слаг", max_length=30, unique=True)
    description = models.CharField("описание", max_length=100)
    points = models.IntegerField("очки рейтинга", default=500)
    bootstrap_icon = models.SlugField(
        "иконка",
        max_length=50,
        default="trophy",
    )
    users = models.ManyToManyField(
        User,
        related_name="achievements",
        blank=True,
        verbose_name="пользователи",
    )
    objects = AchievementManager()

    class Meta:
        verbose_name = "достижение"
        verbose_name_plural = "достижения"

    def __str__(self):
        return self.name
