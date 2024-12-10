from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView

from users.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    FormContext,
)

__all__ = ()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/auth.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return FormContext(
            [self.get_form()],
            title="Регистрация",
            info="Заполните поля, чтобы создать аккаунт",
            description=(
                "Убедитесь, что указали корректный логин и надёжный пароль"
            ),
            submit_button="Создать",
            info_icon="bi-person-plus",
            description_icon="bi-envelope-check",
            submit_button_icon="bi-person-plus",
            footer_items=[
                {
                    "text": "Уже есть аккаунт?",
                    "url": reverse("users:login"),
                    "icon": "bi-box-arrow-in-right",
                    "link_text": "Войти",
                },
            ],
            **kwargs,
        )


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/auth.html"
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs):
        return FormContext(
            [self.get_form()],
            title="Вход",
            info="Заполните поля, чтобы войти",
            description=(
                "Убедитесь, что указали корректный логин и верный пароль"
            ),
            submit_button="Войти",
            info_icon="bi-person-plus",
            description_icon="bi-envelope-check",
            submit_button_icon="bi-box-arrow-in-right",
            footer_items=[
                {
                    "text": "Нет аккаунта?",
                    "url": reverse("users:signup"),
                    "icon": "bi-person-plus-fill",
                    "link_text": "Создать аккаунт",
                },
            ],
            **kwargs,
        )


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "users/profile.html"
    context_object_name = "friends"

    def get_queryset(self):
        return self.request.user.friends.all()
