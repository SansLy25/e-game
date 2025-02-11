import django.test
import django.urls

import planning.views


class PlanningUrlsTests(django.test.TestCase):
    def test_editing_url_resolves(self):
        url = django.urls.reverse("planning:editing")
        self.assertEqual(
            django.urls.resolve(url).func.view_class,
            planning.views.ScheduleEditingView,
        )

    def test_visiting_url_resolves(self):
        url = django.urls.reverse("planning:visiting")
        self.assertEqual(
            django.urls.resolve(url).func.view_class,
            planning.views.VisitingView,
        )
