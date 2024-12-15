from django.urls import path

from users.friends.views import (
    AcceptFriendRequestView,
    AddFriendView,
    FriendsListView,
    RejectFriendRequestView,
    RemoveFriendView,
    SearchResultsView,
)

app_name = "friends"

urlpatterns = [
    path("", FriendsListView.as_view(), name="list"),
    path("search/", SearchResultsView.as_view(), name="search"),
    path("add/<int:pk>/", AddFriendView.as_view(), name="add"),
    path(
        "add/<str:username>/",
        AddFriendView.as_view(),
        name="add_by_username",
    ),
    path("remove/<int:pk>/", RemoveFriendView.as_view(), name="remove"),
    path(
        "accept/<int:pk>/",
        AcceptFriendRequestView.as_view(),
        name="accept",
    ),
    path(
        "reject/<int:pk>/",
        RejectFriendRequestView.as_view(),
        name="reject",
    ),
]
