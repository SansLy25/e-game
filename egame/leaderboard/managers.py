import django.conf
import redis

import users.models


class LeaderboardManager:
    _redis_conn = None
    global_leaderboard = "global_leaderboard"

    @property
    def redis_conn(self):
        if self._redis_conn is None:
            redis_host = getattr(
                django.conf.settings,
                "REDIS_HOST",
                "localhost",
            )
            redis_port = getattr(django.conf.settings, "REDIS_PORT", 6379)
            redis_db = getattr(django.conf.settings, "REDIS_DB", 1)
            self._redis_conn = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
            )

        return self._redis_conn

    def load_initial_data(self):
        users_ = users.models.User.objects.values("id", "score")
        for user in users_:
            self.update_score(user_id=user["id"], score=user["score"])

    def update_score(self, user_id, score):
        self.redis_conn.zadd(self.global_leaderboard, {user_id: score})

    def get_top_users(self, count=100):
        return self.redis_conn.zrevrange(
            self.global_leaderboard,
            0,
            count - 1,
            withscores=True,
        )

    def get_user_rank(self, user_id):
        rank = self.redis_conn.zrevrank(self.global_leaderboard, user_id)
        return rank + 1 if rank is not None else None


class LeaderboardManagerWithDB(LeaderboardManager):
    def update_score_with_db(self, user_id, score):
        self.update_score(user_id=user_id, score=score)

        users.models.User.objects.filter(id=user_id).update(score=score)
