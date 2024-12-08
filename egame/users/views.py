from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from users.forms import CustomUserCreationForm

__all__ = ()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:profile")
    template_name = "users/signup.html"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("users:profile")


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "users/profile.html"
    context_object_name = "friends"

    def get_queryset(self):
        return self.request.user.friends.all()
