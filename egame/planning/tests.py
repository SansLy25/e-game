from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from planning.models import DayOfWeek, VisitedDay


class DayOfWeekModelTest(TestCase):
    def setUp(self):
        self.day_of_week = DayOfWeek.objects.create(day=0)

    def test_day_creation(self):
        self.assertEqual(self.day_of_week.day, 0)
        self.assertEqual(str(self.day_of_week), "Понедельник")

    def test_unique_day(self):
        with self.assertRaises(IntegrityError):
            DayOfWeek.objects.create(day=0)


class VisitedDayModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password",
        )
        self.visited_day = VisitedDay.objects.create(user=self.user)

    def test_visited_day_creation(self):
        self.assertEqual(self.visited_day.user, self.user)
        self.assertIsNotNone(self.visited_day.day)

    def test_related_name(self):
        self.assertEqual(self.user.visited_days.count(), 1)
        self.assertEqual(self.user.visited_days.first(), self.visited_day)
