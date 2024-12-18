import django.db.models.signals
import django.dispatch

import leaderboard.managers
import users.models

leaderboard = leaderboard.managers.LeaderboardManager()


@django.dispatch.receiver(
    django.db.models.signals.post_save,
    sender=users.models.User,
)
def update_leaderboard(sender, instance, **kwargs):
    leaderboard.update_score(instance.id, instance.score)
