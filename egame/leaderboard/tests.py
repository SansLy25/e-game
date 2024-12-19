import django.conf
import django.contrib.auth
import django.test
import django.urls

import leaderboard.views
import users.models

User = django.contrib.auth.get_user_model()


class LeaderboardViewsTestCase(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.users = [
            User.objects.create_user(username=f"user{i}", score=i * 10)
            for i in range(1, 105)
        ]

        cls.test_user = cls.users[0]
        cls.test_user.friends.set(cls.users[1:51])
        cls.test_user_friends = cls.test_user.friends.all().count()

        cls.test_user_2 = cls.users[51]
        cls.test_user_2.friends.set(cls.users[1:101])
        cls.test_user_2_friends = cls.test_user_2.friends.all().count()

        cls.global_leaderboard_url = django.urls.reverse(
            "leaderboard:global_leaderboard",
        )
        cls.friends_leaderboard_url = django.urls.reverse(
            "leaderboard:friends_leaderboard",
        )

    def setUp(self):
        self.client.force_login(self.test_user)

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(LeaderboardViewsTestCase, self).tearDown()

    def test_global_leaderboard_accessible(self):
        response = self.client.get(self.global_leaderboard_url)
        self.assertEqual(
            response.status_code,
            200,
            msg="Глобальная таблица лидеров недоступна. Ожидался статус 200.",
        )

    def test_global_leaderboard_context(self):
        response = self.client.get(self.global_leaderboard_url)
        top_users = response.context["top_users"]
        total_users = response.context["total_users"]

        self.assertEqual(
            len(top_users),
            leaderboard.views.GLOBAL_TOP_LIMIT,
            msg=(
                f"Неверное количество пользователей в глобальном лидерборде. "
                f"Ожидалось {leaderboard.views.GLOBAL_TOP_LIMIT}, "
                f"получено {len(top_users)}."
            ),
        )
        self.assertEqual(
            total_users,
            User.objects.count(),
            msg=(
                f"Общее количество пользователей неверно. "
                f"Ожидалось {User.objects.count()}, получено {total_users}."
            ),
        )

        scores = [user["score"] for user in top_users]
        self.assertTrue(
            all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)),
            msg=(
                "Пользователи в глобальном лидерборде "
                "не отсортированы по убыванию баллов."
            ),
        )

    def test_friends_leaderboard_accessible(self):
        response = self.client.get(self.friends_leaderboard_url)
        self.assertEqual(
            response.status_code,
            200,
            msg="Таблица друзей недоступна. Ожидался статус 200.",
        )

    def test_friends_leaderboard_context(self):
        response = self.client.get(self.friends_leaderboard_url)
        friends_leaderboard = response.context["friends_leaderboard"]
        total_user_friends = response.context["total_user_friends"]

        expected_count = (
            self.test_user_friends + 1
            if self.test_user
            in [friend["user"] for friend in friends_leaderboard]
            else leaderboard.views.FRIENDS_TOP_LIMIT
        )

        self.assertEqual(
            len(friends_leaderboard),
            expected_count,
            msg=(
                f"Неверное количество друзей в таблице друзей. "
                f"Ожидалось {expected_count} друзей и сам пользователь, "
                f"получено {len(friends_leaderboard)}."
            ),
        )
        self.assertEqual(
            total_user_friends,
            self.test_user.friends.count(),
            msg=(
                f"Общее количество друзей неверно. "
                f"Ожидалось {self.test_user.friends.count()}, "
                f"получено {total_user_friends}."
            ),
        )

        scores = [friend["score"] for friend in friends_leaderboard]
        self.assertTrue(
            all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)),
            msg="Друзья в таблице друзей не отсортированы по убыванию баллов.",
        )

    def test_friends_leaderboard_large_friend_list(self):
        self.client.force_login(self.test_user_2)
        response = self.client.get(self.friends_leaderboard_url)
        friends_leaderboard = response.context["friends_leaderboard"]

        expected_count = (
            self.test_user_2_friends
            if self.test_user_2
            in [friend["user"] for friend in friends_leaderboard]
            else leaderboard.views.FRIENDS_TOP_LIMIT
        )

        self.assertEqual(
            len(friends_leaderboard),
            expected_count,
            msg=(
                f"Неверное количество друзей в таблице друзей для "
                f"пользователя с более чем 100 друзьями. "
                f"Ожидалось {expected_count}, "
                f"у пользователя низкий рейтинг, "
                f"он не должен входить в топ "
                f"{leaderboard.views.FRIENDS_TOP_LIMIT}, "
                f"получено {len(friends_leaderboard)}."
            ),
        )

    def test_current_user_container_visibility(self):
        self.client.force_login(self.users[0])
        response = self.client.get(self.global_leaderboard_url)
        current_user_data = response.context["current_user_data"]

        self.assertIsNotNone(
            current_user_data,
            msg=(
                "Контейнер текущего пользователя не отображается, "
                "хотя он не входит в топ-100."
            ),
        )
