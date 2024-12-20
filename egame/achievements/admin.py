from django.contrib import admin

from achievements.models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description", "points", "bootstrap_icon")
    search_fields = ("name", "slug")
    filter_horizontal = ("users",)
