from django.utils.timezone import localtime, now, timedelta

from planning.models import VisitedDay


class VisitingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            today = localtime(now()).date()

            if not VisitedDay.objects.filter(user=user, day=today).exists():
                VisitedDay.objects.create(user=user, day=today)
                if today.weekday() in user.days_of_lessons.values_list(
                    "day",
                    flat=True,
                ):
                    user.score += 100
                    user.score_planning += 100
                else:
                    user.score += 50
                    user.score_planning += 50

                user.save()

            cutoff_date = now().date() - timedelta(days=30)
            VisitedDay.objects.filter(user=user, day__lt=cutoff_date).delete()

        return self.get_response(request)
