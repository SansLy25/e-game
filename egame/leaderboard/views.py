import django.contrib.auth
import django.contrib.auth.mixins
import django.views.generic

import leaderboard.managers

User = django.contrib.auth.get_user_model()
leaderboard = leaderboard.managers.LeaderboardManager()


class GlobalLeaderboardView(django.views.generic.TemplateView):
    template_name = "leaderboard/global.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_users = leaderboard.get_top_users(100)

        user_ids = [int(user_id) for user_id, _ in top_users]

        users = User.objects.filter(id__in=user_ids)
        user_map = {user.id: user for user in users}

        total_users = User.objects.count()

        user_data = [
            {
                "user": user_map[int(user_id)],
                "score": int(score),
                "rank": rank + 1,
            }
            for rank, (user_id, score) in enumerate(top_users)
            if int(user_id) in user_map
        ]

        current_user_rank = leaderboard.get_user_rank(self.request.user.id)
        is_on_top = any(
            (int(user_id) == self.request.user.id for user_id, _ in top_users),
        )

        current_user_data = None

        if not is_on_top and current_user_rank is not None:
            current_user_score = leaderboard.redis_conn.zscore(
                leaderboard.global_leaderboard,
                self.request.user.id,
            )
            current_user_data = {
                "user": self.request.user,
                "score": int(current_user_score),
                "rank": current_user_rank,
            }

        context.update(
            {
                "top_users": user_data,
                "current_user_rank": current_user_rank,
                "current_user_data": current_user_data,
                "is_on_top": is_on_top,
                "total_users": total_users,
            },
        )

        return context


class FriendsLeaderboardView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.TemplateView,
):
    template_name = "leaderboard/friends.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        friends = self.request.user.friends.all()
        friends_ids = [friend.id for friend in friends] + [
            self.request.user.id,
        ]

        total_user_friends = self.request.user.friends.count()

        friends_users = User.objects.filter(id__in=friends_ids)
        user_map = {user.id: user for user in friends_users}

        top_friends = [
            {
                "user": user_map[friend.id],
                "score": friend.score,
                "rank": leaderboard.get_user_rank(friend.id),
            }
            for friend in friends_users
            if friend.id in user_map
        ]

        top_friends_sorted = sorted(
            top_friends,
            key=lambda x: x["score"],
            reverse=True,
        )

        is_in_top_friends = any(
            friend["user"].id == self.request.user.id
            for friend in top_friends_sorted
        )
        current_user_rank = leaderboard.get_user_rank(self.request.user.id)
        current_user_score = leaderboard.redis_conn.zscore(
            leaderboard.global_leaderboard,
            self.request.user.id,
        )

        current_user_data = None
        if not is_in_top_friends and current_user_rank is not None:
            current_user_data = {
                "user": self.request.user,
                "score": int(current_user_score),
                "rank": current_user_rank,
            }

        context.update(
            {
                "friends_leaderboard": top_friends_sorted,
                "total_user_friends": total_user_friends,
                "current_user_data": current_user_data,
                "is_in_top_friends": is_in_top_friends,
            },
        )

        return context
