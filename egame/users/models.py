from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.db.models import QuerySet
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse

from practice.models import Exam


class UserManager(BaseUserManager):
    def get_by_username_or_pk(self, username: str = None, pk: int = None):
        if username:
            return get_object_or_404(self.model, username=username)

        return get_object_or_404(self.model, pk=pk)

    def search_by_username(
        self,
        username: str,
        exclude_user: Optional["User"] = None,
    ):
        queryset = self.filter(username__icontains=username)
        if exclude_user:
            return queryset.exclude(
                Q(pk=exclude_user.pk) | Q(friends=exclude_user),
            )

        return queryset
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

    objects = UserManager()

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
        solutions = self.get_solutions(exam_slug).order_by("-date", "-id")[
            :8:-1
        ]

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
        solutions = self.get_solutions(exam_slug).order_by("-date", "-id")[
            :8:-1
        ]

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
        exam = Exam.objects.get(slug=exam_slug)

        solutions = Solution.objects.filter(exam=exam, full_variant=True)
        scores = [solution.get_score_percent() for solution in solutions]

        return round(division(sum(scores), solutions.count()), 0)

    @classmethod
    def get_all_users_average_duration(cls, exam_slug) -> int:
        exam = Exam.objects.get(slug=exam_slug)

        solutions = Solution.objects.filter(exam=exam, full_variant=True)
        durations = [solution.duration.seconds for solution in solutions]

        return round(division(sum(durations), solutions.count()), 0)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name="sent_friend_requests",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        User,
        related_name="received_friend_requests",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    class Meta:
        verbose_name = "заявка в друзья"
        verbose_name_plural = "заявки в друзья"
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"От {self.from_user.username} к {self.to_user.username}"

    def accept(self):
        self.from_user.friends.add(self.to_user)
        self.accepted = True
        self.save()

    def reject(self):
        self.rejected = True
        self.save()
