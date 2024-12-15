from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
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
