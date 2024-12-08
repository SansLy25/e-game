from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, TemplateView

from users.forms import UserSearchForm
from users.models import User

__all__ = ()


class FriendListView(LoginRequiredMixin, ListView):
    template_name = "friends/list.html"
    context_object_name = "friends"

    def get_queryset(self):
        return self.request.user.friends.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = UserSearchForm()
        context["friend_link"] = self.request.build_absolute_uri(
            self.request.user.get_friend_link(),
        )
        return context


class UserSearchView(LoginRequiredMixin, TemplateView):
    template_name = "friends/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserSearchForm(self.request.GET)
        users = []

        if form.is_valid() and form.cleaned_data.get("username"):
            username = form.cleaned_data["username"]
            users = User.objects.filter(
                username__icontains=username,
            ).exclude(
                Q(id=self.request.user.id) | Q(friends=self.request.user),
            )

        context["users"] = users
        context["form"] = form
        return context


class AddFriendView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("users:friends:list")

    def get_redirect_url(self, *args, **kwargs):
        try:
            username = kwargs.get("username")
            friend = get_object_or_404(
                User,
                **(
                    {"username": username}
                    if username
                    else {"pk": kwargs.get("pk")}
                ),
            )
            if friend != self.request.user:
                self.request.user.friends.add(friend)
                messages.success(
                    self.request,
                    f"Пользователь {friend.username} добавлен в друзья!",
                )
        except User.DoesNotExist:
            messages.error(self.request, "Пользователь не найден")

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
