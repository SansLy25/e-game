import django.db.utils
import django.test

import planning.models
import users.models


class DayOfWeekTests(django.test.TestCase):
    def test_day_of_week_creation(self):
        day = planning.models.DayOfWeek.objects.create(day=0)
        self.assertEqual(day.day, 0)
        self.assertEqual(str(day), "Понедельник")

    def test_day_of_week_unique_constraint(self):
        planning.models.DayOfWeek.objects.create(day=1)
        with self.assertRaises(django.db.utils.IntegrityError):
            planning.models.DayOfWeek.objects.create(day=1)


class VisitedDayTests(django.test.TestCase):
    def setUp(self):
        self.user = users.models.User.objects.create(username="testuser")

        super(VisitedDayTests, self).setUp()

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(VisitedDayTests, self).tearDown()

    def test_visited_day_creation(self):
        visited_day = planning.models.VisitedDay.objects.create(user=self.user)
        self.assertEqual(visited_day.user, self.user)
        self.assertIsNotNone(visited_day.day)

    def test_visited_day_relationship(self):
        planning.models.VisitedDay.objects.create(user=self.user)
        self.assertEqual(self.user.visited_days.count(), 1)
