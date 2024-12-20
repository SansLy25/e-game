import django.contrib.auth
import django.db.utils
import django.test

import achievements.models
import users.models

User = django.contrib.auth.get_user_model()


class AchievementModelTests(django.test.TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="password1",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="password2",
        )

        self.achievement1 = achievements.models.Achievement.objects.create(
            name="First Achievement",
            slug="first-achievement",
            description="This is the first test achievement.",
            points=1000,
            bootstrap_icon="medal",
        )
        self.achievement2 = achievements.models.Achievement.objects.create(
            name="Second Achievement",
            slug="second-achievement",
            description="This is the second test achievement.",
            points=500,
            bootstrap_icon="star",
        )

        self.achievement1.users.add(self.user1)
        self.achievement2.users.add(self.user2)

        super(AchievementModelTests, self).setUp()

    def tearDown(self):
        users.models.User.objects.all().delete()
        achievements.models.Achievement.objects.all().delete()

        super(AchievementModelTests, self).tearDown()

    def test_achievement_creation(self):
        self.assertEqual(achievements.models.Achievement.objects.count(), 2)
        self.assertEqual(self.achievement1.name, "First Achievement")
        self.assertEqual(self.achievement1.slug, "first-achievement")
        self.assertEqual(
            self.achievement1.description,
            "This is the first test achievement.",
        )
        self.assertEqual(self.achievement1.points, 1000)
        self.assertEqual(self.achievement1.bootstrap_icon, "medal")

    def test_users_related_to_achievements(self):
        self.assertIn(self.user1, self.achievement1.users.all())
        self.assertNotIn(self.user2, self.achievement1.users.all())
        self.assertIn(self.user2, self.achievement2.users.all())

    def test_str_method(self):
        self.assertEqual(str(self.achievement1), "First Achievement")
        self.assertEqual(str(self.achievement2), "Second Achievement")

    def test_manager_by_slug(self):
        achievement = achievements.models.Achievement.objects.by_slug(
            "first-achievement",
        )
        self.assertEqual(achievement, self.achievement1)
