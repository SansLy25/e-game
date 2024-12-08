from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from practice.models import Exam
from users.models import User

__all__ = ()


class FriendsViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(name="Test Exam")
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.friend = User.objects.create_user(
            username="frienduser",
            password="testpass123",
        )
        cls.another_user = User.objects.create_user(
            username="anotheruser",
            password="testpass123",
        )
        cls.user.exams.set([cls.exam])

        cls.friend_list_url = reverse("users:friends:list")
        cls.search_url = reverse("users:friends:search")
        cls.add_friend_url = reverse(
            "users:friends:add",
            kwargs={"pk": cls.friend.pk},
        )
        cls.remove_friend_url = reverse(
            "users:friends:remove",
            kwargs={"pk": cls.friend.pk},
        )
        cls.add_by_username_url = reverse(
            "users:friends:add_by_username",
            kwargs={"username": cls.friend.username},
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="testpass123")


class FriendListViewTest(FriendsViewsTest):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.friend_list_url)
        self.assertRedirects(
            response,
            f"/login/?next={self.friend_list_url}",
        )

    def test_template_used(self):
        response = self.client.get(self.friend_list_url)
        self.assertTemplateUsed(response, "friends/list.html")

    def test_context_data(self):
        self.user.friends.add(self.friend)
        response = self.client.get(self.friend_list_url)
        self.assertIn("friends", response.context)
        self.assertIn("search_form", response.context)
        self.assertIn("friend_link", response.context)
        self.assertIn(self.friend, response.context["friends"])

    def test_friend_link_in_context(self):
        response = self.client.get(self.friend_list_url)
        expected_path = reverse(
            "users:friends:add_by_username",
            kwargs={"username": self.user.username},
        )
        self.assertTrue(
            response.context["friend_link"].endswith(expected_path),
        )


class UserSearchViewTest(FriendsViewsTest):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.search_url)
        self.assertRedirects(
            response,
            f"/login/?next={self.search_url}",
        )

    def test_template_used(self):
        response = self.client.get(self.search_url)
        self.assertTemplateUsed(response, "friends/search_results.html")

    def test_empty_search(self):
        response = self.client.get(self.search_url)
        self.assertEqual(len(response.context["users"]), 0)

    def test_search_with_results(self):
        response = self.client.get(
            self.search_url,
            {"username": "friend"},
        )
        self.assertIn(self.friend, response.context["users"])

    def test_search_excludes_current_user(self):
        response = self.client.get(
            self.search_url,
            {"username": "test"},
        )
        self.assertNotIn(self.user, response.context["users"])

    def test_search_excludes_existing_friends(self):
        self.user.friends.add(self.friend)
        response = self.client.get(
            self.search_url,
            {"username": "friend"},
        )
        self.assertNotIn(self.friend, response.context["users"])


class AddFriendViewTest(FriendsViewsTest):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.add_friend_url)
        self.assertRedirects(
            response,
            f"/login/?next={self.add_friend_url}",
        )

    def test_add_friend_success(self):
        response = self.client.get(self.add_friend_url, follow=True)
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, self.friend_list_url)
        self.assertEqual(len(messages), 1)
        self.assertIn("добавлен в друзья", str(messages[0]))
        self.assertIn(self.friend, self.user.friends.all())

    def test_cannot_add_self_as_friend(self):
        url = reverse("users:friends:add", kwargs={"pk": self.user.pk})
        self.client.get(url, follow=True)
        self.assertNotIn(self.user, self.user.friends.all())

    def test_add_nonexistent_user(self):
        url = reverse("users:friends:add", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RemoveFriendViewTest(FriendsViewsTest):
    def setUp(self):
        super().setUp()
        self.user.friends.add(self.friend)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.remove_friend_url)
        self.assertRedirects(
            response,
            f"/login/?next={self.remove_friend_url}",
        )

    def test_remove_friend_success(self):
        response = self.client.get(self.remove_friend_url, follow=True)
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, self.friend_list_url)
        self.assertEqual(len(messages), 1)
        self.assertIn("удален из друзей", str(messages[0]))
        self.assertNotIn(self.friend, self.user.friends.all())

    def test_remove_nonexistent_user(self):
        url = reverse("users:friends:remove", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class AddFriendByUsernameViewTest(FriendsViewsTest):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.add_by_username_url)
        self.assertRedirects(
            response,
            f"/login/?next={self.add_by_username_url}",
        )

    def test_add_friend_by_username_success(self):
        response = self.client.get(self.add_by_username_url, follow=True)
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, self.friend_list_url)
        self.assertEqual(len(messages), 1)
        self.assertIn("добавлен в друзья", str(messages[0]))
        self.assertIn(self.friend, self.user.friends.all())

    def test_cannot_add_self_by_username(self):
        url = reverse(
            "users:friends:add_by_username",
            kwargs={"username": self.user.username},
        )
        self.client.get(url, follow=True)
        self.assertNotIn(self.user, self.user.friends.all())
