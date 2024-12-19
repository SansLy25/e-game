import django.test
import django.urls

import practice.models
import users.models


class UserModelTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = practice.models.Exam.objects.create(name="Test Exam")
        users.models.DayOfWeek.objects.create(day=0)
        cls.user = users.models.User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.friend = users.models.User.objects.create_user(
            username="frienduser",
            password="testpass123",
        )
        cls.user.exams.set([cls.exam])

    def tearDown(self):
        users.models.User.objects.all().delete()
        practice.models.Exam.objects.all().delete()
        users.models.DayOfWeek.objects.all().delete()

        super(UserModelTest, self).tearDown()

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "testuser")

    def test_user_exam_relationship(self):
        self.assertEqual(self.user.exams.last(), self.exam)

    def test_user_verbose_names(self):
        self.assertEqual(
            users.models.User._meta.verbose_name,
            "пользователь",
        )
        self.assertEqual(
            users.models.User._meta.verbose_name_plural,
            "пользователи",
        )

    def test_exam_can_be_null(self):
        user = users.models.User.objects.create_user(
            username="testuser2",
            password="testpass123",
        )
        self.assertFalse(user.exams.exists())

    def test_add_friend(self):
        self.user.friends.add(self.friend)
        self.assertIn(self.friend, self.user.friends.all())
        self.assertIn(self.user, self.friend.friends.all())

    def test_remove_friend(self):
        self.user.friends.add(self.friend)
        self.user.friends.remove(self.friend)
        self.assertNotIn(self.friend, self.user.friends.all())
        self.assertNotIn(self.user, self.friend.friends.all())

    def test_get_friend_link(self):
        expected_url = django.urls.reverse(
            "users:friends:add_by_username",
            args=[self.user.username],
        )
        self.assertEqual(self.user.get_friend_link(), expected_url)
