from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from practice.models import Exam
from users.models import FriendRequest


class UserModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1",
            password="password1",
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="password2",
        )
        self.exam = Exam.objects.create(slug="exam1", name="Exam 1")

    def test_create_user(self):
        self.assertEqual(self.user1.username, "user1")
        self.assertEqual(self.user2.username, "user2")

    def test_get_friend_link(self):
        link = self.user1.get_friend_link()
        expected_link = f"/friends/add/{self.user1.username}/"
        self.assertEqual(link, expected_link)

    def test_add_friend(self):
        self.user1.friends.add(self.user2)
        self.assertIn(self.user2, self.user1.friends.all())
        self.assertIn(self.user1, self.user2.friends.all())


class FriendRequestModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1",
            password="password1",
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="password2",
        )

    def test_send_friend_request(self):
        friend_request = FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2,
        )
        self.assertEqual(friend_request.from_user, self.user1)
        self.assertEqual(friend_request.to_user, self.user2)

    def test_accept_friend_request(self):
        friend_request = FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2,
        )
        friend_request.accept()
        self.assertTrue(friend_request.accepted)
        self.assertIn(self.user2, self.user1.friends.all())
        self.assertIn(self.user1, self.user2.friends.all())

    def test_reject_friend_request(self):
        friend_request = FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2,
        )
        friend_request.reject()
        self.assertTrue(friend_request.rejected)

    def test_unique_friend_request(self):
        FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        with self.assertRaises(IntegrityError):
            FriendRequest.objects.create(
                from_user=self.user1,
                to_user=self.user2,
            )

    def test_reverse_friend_request(self):
        FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2,
        )
        reverse_request = FriendRequest.objects.filter(
            from_user=self.user2,
            to_user=self.user1,
        )
        self.assertEqual(reverse_request.count(), 0)
