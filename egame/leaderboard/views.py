import django.contrib.auth
import django.contrib.auth.mixins
import django.db.models
import django.db.models.functions
import django.views.generic

GLOBAL_TOP_LIMIT = 100
FRIENDS_TOP_LIMIT = 100


User = django.contrib.auth.get_user_model()


class GlobalLeaderboardView(django.views.generic.TemplateView):
    template_name = "leaderboard/global.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_users = User.objects.all().order_by("-score")[:GLOBAL_TOP_LIMIT]

        total_users = User.objects.count()

        user_data = [
            {
                "user": user,
                "score": user.score,
                "rank": rank + 1,
            }
            for rank, user in enumerate(top_users)
        ]

        current_user = self.request.user
        current_user_rank = (
            User.objects.filter(score__gt=current_user.score).count() + 1
            if current_user.is_authenticated
            else None
        )

        is_on_top = any(user.id == current_user.id for user in top_users)

        current_user_data = None
        if not is_on_top and current_user.is_authenticated:
            current_user_data = {
                "user": current_user,
                "score": current_user.score,
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

        users_with_filter = User.objects.filter(id__in=friends_ids)

        friends_users = (
            users_with_filter.annotate(
                rank=django.db.models.Window(
                    expression=django.db.models.functions.Rank(),
                    order_by=django.db.models.F("score").desc(),
                ),
            ).order_by("-score")
        )[:FRIENDS_TOP_LIMIT]

        total_user_friends = friends.count()

        top_friends = [
            {
                "user": friend,
                "score": friend.score,
                "rank": friend.rank,
            }
            for friend in friends_users
        ]

        is_in_top_friends = any(
            friend["user"].id == self.request.user.id for friend in top_friends
        )

        current_user_data = None
        if not is_in_top_friends:
            current_user = self.request.user
            current_user_data = {
                "user": current_user,
                "score": current_user.score,
                "rank": (
                    User.objects.filter(score__gt=current_user.score).count()
                    + 1
                ),
            }

        context.update(
            {
                "friends_leaderboard": top_friends,
                "total_user_friends": total_user_friends,
                "current_user_data": current_user_data,
                "is_in_top_friends": is_in_top_friends,
            },
        )

        return context
