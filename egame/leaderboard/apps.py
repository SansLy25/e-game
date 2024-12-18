import django.apps


class LeaderboardConfig(django.apps.AppConfig):
    name = "leaderboard"
    verbose_name = "Leaderboard"

    def ready(self):
        import leaderboard.signals  # noqa: F401
