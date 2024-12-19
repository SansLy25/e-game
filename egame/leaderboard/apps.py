import django.apps


class LeaderboardConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leaderboard"
    verbose_name = "Таблица лидеров"
