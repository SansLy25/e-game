from django.contrib.auth.views import LogoutView
from django.urls import include, path

from users import views
import users.friends.urls

app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="users:login"),
        name="logout",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("friends/", include(users.friends.urls, namespace="friends")),
    path(
        "achievements/",
        views.AchievementsListView.as_view(),
        name="achievements_list",
    ),
]
