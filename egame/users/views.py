from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from achievements.models import Achievement
from users.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    FormAdditions,
    FormButton,
    FormContext,
    FormFooterItem,
)


class FromContextView:
    form_context: FormContext

    def get_context_data(self, **kwargs):
        return self.form_context(self, kwargs)


class SignUpView(FromContextView, CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/auth.html"
    success_url = reverse_lazy("users:profile")
    form_context = FormContext(
        "Регистрация",
        FormAdditions(
            "Заполните поля, чтобы создать аккаунт",
            "bi-person-plus",
        ),
        FormAdditions(
            "Убедитесь, что указали корректный логин и надёжный пароль",
            "bi-envelope-check",
        ),
        FormButton("Создать", "bi-person-plus"),
        None,
        FormFooterItem(
            "Уже есть аккаунт?",
            "bi-box-arrow-in-right",
            reverse_lazy("users:login"),
            "Войти",
        ),
    )

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(FromContextView, LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/auth.html"
    success_url = reverse_lazy("users:profile")
    form_context = FormContext(
        "Вход",
        None,
        FormAdditions(
            "Войдите, чтобы продолжить",
            "bi-door-open",
        ),  # Updated description
        FormButton("Войти", "bi-box-arrow-in-right"),
        None,
        FormFooterItem(
            "Нет аккаунта?",
            "bi-person-plus-fill",
            reverse_lazy("users:signup"),
            "Создать",
        ),
    )


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "users/profile.html"
    context_object_name = "friends"

    def get_queryset(self):
        return self.request.user.friends.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["achievements"] = self.request.user.achievements.all()
        return context


class AchievementsListView(LoginRequiredMixin, ListView):
    template_name = "users/achievements_list.html"
    context_object_name = "achievements"

    def get_queryset(self):
        return Achievement.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_achievements"] = self.request.user.achievements.all()
        return context
