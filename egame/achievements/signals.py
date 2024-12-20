from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from achievements.models import Achievement
from practice.models import Exam, Solution
from users.models import User


@receiver(post_save, sender=Solution)
def check_solution_achievements(sender, instance: Solution, created, **kwargs):
    if not created:
        return

    user = instance.user
    if not user:
        return

    exam = instance.exam

    check_math_master_achievement(user, exam, instance)
    check_sprinter_achievement(user, instance)
    check_perfect_achievement(user, instance)
    check_marathoner_achievement(user, exam)
    check_accurate_achievement(user, exam)
    check_fast_and_accurate_achievement(user, instance)
    check_wunderkind_achievement(user)
    check_consistent_achievement(user)


@receiver(post_save, sender=User)
def check_user_achievements(sender, instance: User, created, **kwargs):
    if not created:
        return

    if instance.friends.count() >= 10:
        add_achievement(instance, "social-butterfly")

    if instance.received_friend_requests.filter(accepted=True).count() >= 5:
        add_achievement(instance, "friendly")

    if instance.sent_friend_requests.count() >= 5:
        add_achievement(instance, "outgoing")

    if instance.total_time_spent >= 360000:
        add_achievement(instance, "regular")


def add_achievement(user: User, achievement_slug: str):
    achievement = Achievement.objects.by_slug(achievement_slug)
    if not user.achievements.contains(achievement):
        user.achievements.add(achievement)
        user.score += achievement.points
        user.save()


def check_accuracy(user: User, exam_slug: str, count: int, accuracy: int):
    solutions = user.get_solutions(exam_slug).order_by("-date", "-id")[:count]
    if solutions.count() < count:
        return False

    for solution in solutions:
        if solution.get_score_percent() < accuracy:
            return False

    return True


def check_all_exams_max_score(user: User):
    for exam in user.exams.all():
        if (
            not user.get_solutions(exam.slug)
            .filter(score=models.F("max_score"))
            .exists()
        ):
            return False

    return True


def check_daily_solving(user: User, days: int):
    from datetime import timedelta

    today = timezone.now().date()
    for i in range(days):
        date = today - timedelta(days=i)
        if not user.solutions.filter(date=date).exists():
            return False

    return True


def check_math_master_achievement(user: User, exam: Exam, instance: Solution):
    if (
        exam.slug == "math"
        and instance.full_variant is False
        and user.get_solutions(exam.slug, full_variant=False).count() >= 100
    ):
        add_achievement(user, "math-master")


def check_sprinter_achievement(user: User, instance: Solution):
    if instance.full_variant and instance.duration.seconds < 30 * 60:
        add_achievement(user, "sprinter")


def check_perfect_achievement(user: User, instance: Solution):
    if instance.full_variant and instance.score == instance.max_score:
        add_achievement(user, "perfect")


def check_marathoner_achievement(user: User, exam: Exam):
    if user.get_solutions(exam.slug).count() >= 10:
        add_achievement(user, "marathoner")


def check_accurate_achievement(user: User, exam: Exam):
    if check_accuracy(user, exam.slug, 5, 90):
        add_achievement(user, "accurate")


def check_fast_and_accurate_achievement(user: User, instance: Solution):
    if (
        instance.full_variant
        and instance.duration.seconds < 45 * 60
        and instance.get_score_percent() >= 80
    ):
        add_achievement(user, "fast-and-accurate")


def check_wunderkind_achievement(user: User):
    if check_all_exams_max_score(user):
        add_achievement(user, "wunderkind")


def check_consistent_achievement(user: User):
    if check_daily_solving(user, 7):
        add_achievement(user, "consistent")
