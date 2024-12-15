from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, TemplateView

from users.forms import UserSearchForm
from users.message import Message
from users.models import FriendRequest, User


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = "friends/list.html"
    context_object_name = "friends"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = (
            user.friends.all().prefetch_related("exams").order_by("username")
        )

        form = UserSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if username:
                return queryset.filter(username__icontains=username)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["search_form"] = UserSearchForm(self.request.GET)
        context["pending_requests"] = user.received_friend_requests.filter(
            accepted=False,
            rejected=False,
        )
        return context


class UserSearchView(LoginRequiredMixin, ListView):
    template_name = "friends/search_results.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        form = UserSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("username"):
            username = form.cleaned_data["username"]
            return User.objects.filter(
                username__icontains=username,
            ).exclude(
                Q(id=self.request.user.id) | Q(friends=self.request.user),
            )

        return User.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserSearchForm(self.request.GET)
        return context


class SearchResultsView(LoginRequiredMixin, ListView):
    template_name = "friends/search_results.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        form = UserSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if username and username.strip():
                return User.objects.search_by_username(
                    username,
                    exclude_user=self.request.user,
                ).prefetch_related("exams")[:5]

            return User.objects.none()

        return User.objects.none()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=UserSearchForm(self.request.GET),
            **kwargs,
        )


class AddFriendView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("users:friends:list")

    def get_redirect_url(self, *args, **kwargs):
        message = Message(self.request)
        try:
            to_user = User.objects.get_by_username_or_pk(**kwargs)
            if to_user != self.request.user:
                if not FriendRequest.objects.filter(
                    from_user=self.request.user,
                    to_user=to_user,
                ).exists():
                    FriendRequest.objects.create(
                        from_user=self.request.user,
                        to_user=to_user,
                    )
                    message.success(
                        "Заявка в друзья пользователю"
                        f" {to_user.username} отправлена!",
                    )
                else:
                    message.warning(
                        "Заявка в друзья пользователю"
                        f" {to_user.username} уже отправлена.",
                    )
            else:
                message.error("Нельзя добавить себя в друзья.")
        except User.DoesNotExist:
            message.error("Пользователь не найден")

        return super().get_redirect_url(*args, **kwargs)


class RemoveFriendView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("users:friends:list")

    def get_redirect_url(self, *args, **kwargs):
        friend = get_object_or_404(User, pk=kwargs["pk"])
        self.request.user.friends.remove(friend)
        messages.success(
            self.request,
            f"Пользователь {friend.username} удален из друзей",
        )
        return super().get_redirect_url(*args, **kwargs)


class AcceptFriendRequestView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("users:friends:list")

    def get_redirect_url(self, *args, **kwargs):
        friend_request = get_object_or_404(
            FriendRequest,
            pk=kwargs["pk"],
            to_user=self.request.user,
            accepted=False,
            rejected=False,
        )
        friend_request.accept()
        message = (
            "Вы подружились с пользователем"
            f" {friend_request.from_user.username}"
        )
        messages.success(self.request, message)
        return super().get_redirect_url(*args, **kwargs)


class RejectFriendRequestView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("users:friends:list")

    def get_redirect_url(self, *args, **kwargs):
        friend_request = get_object_or_404(
            FriendRequest,
            pk=kwargs["pk"],
            to_user=self.request.user,
            accepted=False,
            rejected=False,
        )
        friend_request.reject()
        message = (
            "Вы отклонили заявку пользователя"
            f" {friend_request.from_user.username}"
        )
        messages.info(self.request, message)
        return super().get_redirect_url(*args, **kwargs)


class UserCardView(TemplateView):
    template_name = "friends/user_card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.GET.get("user_id")
        context["user"] = get_object_or_404(
            User.objects.prefetch_related("exams"),
            pk=user_id,
        )
        return context
