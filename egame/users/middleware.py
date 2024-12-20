from django.db import models
from django.http import HttpRequest
from django.utils import timezone

from users.models import User


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated:
            now = timezone.now()
            last_seen = request.user.last_seen
            if last_seen:
                time_spent = (now - last_seen).total_seconds()
                User.objects.filter(pk=request.user.pk).update(
                    total_time_spent=models.F("total_time_spent") + time_spent,
                    last_seen=now,
                )
            else:
                User.objects.filter(pk=request.user.pk).update(last_seen=now)

        return self.get_response(request)
