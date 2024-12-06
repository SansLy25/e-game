from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from users.forms import CustomUserCreationForm
from users.models import User

__all__ = ()


class SignUpView(CreateView):
    model = User
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


@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    template_name = "users/profile.html"
