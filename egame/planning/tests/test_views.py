import django.test
import django.urls

import planning.views
import users.models


class ScheduleEditingViewTests(django.test.TestCase):
    def setUp(self):
        self.factory = django.test.RequestFactory()
        self.user = users.models.User.objects.create_user(
            username="testuser",
            password="password",
        )

        super(ScheduleEditingViewTests, self).setUp()

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(ScheduleEditingViewTests, self).tearDown()

    def test_get_object_returns_logged_in_user(self):
        request = self.factory.get(django.urls.reverse("planning:editing"))
        request.user = self.user
        view = planning.views.ScheduleEditingView()
        view.request = request
        obj = view.get_object()
        self.assertEqual(obj, self.user)

    def test_get_success_url(self):
        view = planning.views.ScheduleEditingView()
        self.assertEqual(
            view.get_success_url(),
            django.urls.reverse("homepage:home"),
        )


class VisitingViewTests(django.test.TestCase):
    def setUp(self):
        self.factory = django.test.RequestFactory()
        self.user = users.models.User.objects.create_user(
            username="testuser",
            password="password",
        )

        super(VisitingViewTests, self).setUp()

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(VisitingViewTests, self).tearDown()

    def test_get_context_data(self):
        request = self.factory.get(django.urls.reverse("planning:visiting"))
        request.user = self.user
        view = planning.views.VisitingView()
        view.request = request
        context = view.get_context_data()
        self.assertIn("all_month_days", context)
        self.assertIn("skipped_days", context)

    def test_get_month_days(self):
        days = planning.views.VisitingView.get_month_days()
        self.assertGreater(len(days), 0)
        self.assertEqual(days[0].day, 1)
