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

            cutoff_date = now().date() - timedelta(days=30)
            VisitedDay.objects.filter(user=user, day__lt=cutoff_date).delete()

        return self.get_response(request)
