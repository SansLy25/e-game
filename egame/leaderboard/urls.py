import django.urls

import leaderboard.views

app_name = "leaderboard"


urlpatterns = [
    django.urls.path(
        "",
        leaderboard.views.GlobalLeaderboardView.as_view(),
        name="global_leaderboard",
    ),
    django.urls.path(
        "friends/",
        leaderboard.views.FriendsLeaderboardView.as_view(),
        name="friends_leaderboard",
    ),
]
