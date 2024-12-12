from django.contrib import admin

from users.models import User

__all__ = ()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff", "is_superuser")
    filter_horizontal = ("exams",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Права доступа",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Дополнительно", {"fields": ("exams",)}),
    )
