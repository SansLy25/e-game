from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

__all__ = ()


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
]
