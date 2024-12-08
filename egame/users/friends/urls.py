from django.urls import path

from users.friends import views

app_name = "friends"

urlpatterns = [
    path("", views.FriendListView.as_view(), name="list"),
    path("search/", views.UserSearchView.as_view(), name="search"),
    path("add/<int:pk>/", views.AddFriendView.as_view(), name="add"),
    path("remove/<int:pk>/", views.RemoveFriendView.as_view(), name="remove"),
    path(
        "add/<str:username>/",
        views.AddFriendByUsernameView.as_view(),
        name="add_by_username",
    ),
]
