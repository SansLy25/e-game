import django.conf
import django.contrib.auth
import django.test

import leaderboard.managers

User = django.contrib.auth.get_user_model()


class LeaderboardTestCase(django.test.TestCase):
    def setUp(self):
        self.leaderboard = leaderboard.managers.LeaderboardManagerWithDB()
        self.redis_conn = self.leaderboard.redis_conn

        self.redis_conn.flushdb()

        self.user1 = User.objects.create_user(username="user1", score=100)
        self.user2 = User.objects.create_user(username="user2", score=200)
        self.user3 = User.objects.create_user(username="user3", score=300)

        self.leaderboard.update_score_with_db(self.user1.id, self.user1.score)
        self.leaderboard.update_score_with_db(self.user2.id, self.user2.score)
        self.leaderboard.update_score_with_db(self.user3.id, self.user3.score)

    def tearDown(self):
        self.redis_conn.flushdb()

    def test_update_score(self):
        new_score = 500

        self.leaderboard.update_score_with_db(
            user_id=self.user1.id,
            score=new_score,
        )

        redis_score = int(
            self.redis_conn.zscore(
                self.leaderboard.global_leaderboard,
                self.user1.id,
            ),
        )
        self.assertEqual(
            redis_score,
            new_score,
            "Score в Redis должен обновиться",
        )

        self.user1.refresh_from_db()
        self.assertEqual(
            self.user1.score,
            new_score,
            "Score в базе данных должен обновиться",
        )

    def test_get_top_users(self):
        top_users = self.leaderboard.get_top_users(3)

        expected_order = [self.user3.id, self.user2.id, self.user1.id]
        actual_order = [int(user_id) for user_id, _ in top_users]

        self.assertEqual(
            expected_order,
            actual_order,
            "Пользователи должны быть в порядке убывания очков",
        )

    def test_get_user_rank(self):
        rank_user1 = self.leaderboard.get_user_rank(self.user1.id)
        rank_user2 = self.leaderboard.get_user_rank(self.user2.id)
        rank_user3 = self.leaderboard.get_user_rank(self.user3.id)

        self.assertEqual(rank_user3, 1, "user3 должен быть на 1 месте")
        self.assertEqual(rank_user2, 2, "user2 должен быть на 2 месте")
        self.assertEqual(rank_user1, 3, "user1 должен быть на 3 месте")

    def test_load_initial_data(self):
        self.redis_conn.flushdb()
        self.leaderboard.load_initial_data()

        redis_count = self.redis_conn.zcard(
            self.leaderboard.global_leaderboard,
        )
        db_count = User.objects.count()

        self.assertEqual(
            redis_count,
            db_count,
            "Количество пользователей в Redis и БД должно совпадать",
        )

    def test_nonexistent_user_rank(self):
        non_user_id = 999
        rank = self.leaderboard.get_user_rank(non_user_id)
        self.assertIsNone(
            rank,
            "Ранг несуществующего пользователя должен быть None",
        )
