from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse

from practice.models import Exam, Solution


def division(a, b):  # Нужно, чтобы избежать деления на 0
    if b == 0:
        return 0

    return a / b


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

    def get_solutions(self, exam_slug, full_variant=True) -> QuerySet:
        exam = Exam.objects.get(slug=exam_slug)

        if full_variant:
            return Solution.objects.filter(
                exam=exam,
                user=self,
                full_variant=full_variant,
            )

        return Solution.objects.filter(
            exam=exam,
            user=self,
        )

    def get_exam_average_score(self, exam_slug) -> float:
        solutions = self.get_solutions(exam_slug)
        scores = [solution.get_score_percent() for solution in solutions]

        return round(division(sum(scores), len(scores)), 0)

    def get_exam_average_duration(self, exam_slug) -> int:
        solutions = self.get_solutions(exam_slug)
        durations = [solution.duration.seconds for solution in solutions]

        return int(round(division(sum(durations), len(durations)), 0))

    def get_score_dynamic(self, exam_slug) -> list:
        solutions = self.get_solutions(exam_slug).order_by("date")[:8]

        dynamic = []
        for solution in solutions:
            score = solution.get_score_percent()
            dynamic.append({"score": score, "date": solution.date})

        return dynamic

    def get_average_variant_size(self, exam_slug) -> float:
        solutions = self.get_solutions(exam_slug, full_variant=False)
        task_counts = [solution.max_score for solution in solutions]

        return round(division(sum(task_counts), len(task_counts)), 1)

    def get_time_dynamic(self, exam_slug) -> list:
        solutions = self.get_solutions(exam_slug).order_by("date")[:8]

        dynamic = []
        for solution in solutions:
            dynamic.append(
                {"duration": solution.duration.seconds, "date": solution.date},
            )

        return dynamic

    def get_friends_average_scores(self, exam_slug) -> dict:
        friends = self.friends.all()
        scores = {}
        for friend in friends:
            score = friend.get_exam_average_score(exam_slug)
            scores[friend.username] = score

        return scores

    @classmethod
    def get_all_users_average_score(cls, exam_slug) -> float:
        average_scores = []

        users = cls.objects.filter(solutions__isnull=False)
        for user in users:
            average_scores.append(user.get_exam_average_score(exam_slug))

        return round(division(sum(average_scores), len(average_scores)), 0)

    @classmethod
    def get_all_users_average_duration(cls, exam_slug) -> int:
        average_durations = []
        users = cls.objects.filter(solutions__isnull=False)
        for user in users:
            average_durations.append(user.get_exam_average_duration(exam_slug))

        return int(
            round(division(sum(average_durations), len(average_durations)), 0),
        )
