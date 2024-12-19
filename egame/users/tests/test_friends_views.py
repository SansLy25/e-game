import http

import django.contrib.auth
import django.test
import django.urls

import users.models

User = django.contrib.auth.get_user_model()


class FriendsListViewTest(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.client.login(username="testuser", password="password")

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(FriendsListViewTest, self).tearDown()

    def test_friends_list_view(self):
        response = self.client.get(django.urls.reverse("users:friends:list"))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "friends/list.html")
        self.assertIn("friends", response.context)
        self.assertIn("pending_requests", response.context)
        self.assertIn("search_form", response.context)


class UserSearchViewTest(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="password",
        )
        self.client.login(username="testuser", password="password")

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(UserSearchViewTest, self).tearDown()

    def test_user_search_view(self):
        response = self.client.get(
            django.urls.reverse("users:friends:search"),
            {"username": "other"},
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "friends/search_results.html")
        self.assertIn("users", response.context)
        self.assertIn(self.other_user, response.context["users"])


class AddFriendViewTest(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="password",
        )
        self.client.login(username="testuser", password="password")

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(AddFriendViewTest, self).tearDown()

    def test_add_friend(self):
        response = self.client.get(
            django.urls.reverse(
                "users:friends:add",
                kwargs={"pk": self.other_user.pk},
            ),
        )
        self.assertRedirects(
            response,
            django.urls.reverse("users:friends:list"),
        )
        self.assertTrue(
            users.models.FriendRequest.objects.filter(
                from_user=self.user,
                to_user=self.other_user,
            ).exists(),
        )


class RemoveFriendViewTest(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.friend = User.objects.create_user(
            username="frienduser",
            password="password",
        )
        self.user.friends.add(self.friend)
        self.client.login(username="testuser", password="password")

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(RemoveFriendViewTest, self).tearDown()

    def test_remove_friend(self):
        response = self.client.get(
            django.urls.reverse(
                "users:friends:remove",
                kwargs={"pk": self.friend.pk},
            ),
        )
        self.assertRedirects(
            response,
            django.urls.reverse("users:friends:list"),
        )
        self.assertNotIn(self.friend, self.user.friends.all())


class AcceptFriendRequestViewTest(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="password",
        )
        self.friend_request = users.models.FriendRequest.objects.create(
            from_user=self.other_user,
            to_user=self.user,
        )
        self.client.login(username="testuser", password="password")

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(AcceptFriendRequestViewTest, self).tearDown()

    def test_accept_friend_request(self):
        response = self.client.get(
            django.urls.reverse(
                "users:friends:accept",
                kwargs={"pk": self.friend_request.pk},
            ),
        )
        self.assertRedirects(
            response,
            django.urls.reverse("users:friends:list"),
        )
        self.assertIn(self.other_user, self.user.friends.all())


class RejectFriendRequestViewTest(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="password",
        )
        self.friend_request = users.models.FriendRequest.objects.create(
            from_user=self.other_user,
            to_user=self.user,
        )
        self.client.login(username="testuser", password="password")

    def tearDown(self):
        users.models.User.objects.all().delete()

        super(RejectFriendRequestViewTest, self).tearDown()

    def test_reject_friend_request(self):
        response = self.client.get(
            django.urls.reverse(
                "users:friends:reject",
                kwargs={"pk": self.friend_request.pk},
            ),
        )
        self.assertRedirects(
            response,
            django.urls.reverse("users:friends:list"),
        )
        self.friend_request.refresh_from_db()
        self.assertTrue(self.friend_request.rejected)
