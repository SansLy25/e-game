from datetime import date, timedelta

from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views.generic import TemplateView, UpdateView

from planning.forms import LessonsDaysEditForm
from users.models import User


class ScheduleEditingView(UpdateView):
    model = User
    form_class = LessonsDaysEditForm
    template_name = "planning/editing.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("homepage:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_days"] = self.request.user.days_of_lessons.values_list(
            "id",
            flat=True,
        )

        return context


class VisitingView(TemplateView):
    template_name = "planning/visiting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = localtime().date()
        user = self.request.user

        user_visited_days = (
            user.visited_days.all()
            .order_by("day")
            .values_list("day", flat=True)
        )

        user_required_week_days = user.days_of_lessons.values_list(
            "day",
            flat=True,
        )
        all_month_days = []
        month_days = self.get_month_days()

        for day in month_days:
            all_month_days.append(
                {
                    "day": day.day,
                    "required": (
                        day.weekday() in user_required_week_days
                        if day <= today
                        else False
                    ),
                    "visited": day in user_visited_days,
                    "is_today": day == today,
                },
            )

        context["all_month_days"] = all_month_days
        context["skipped_days"] = range(month_days[0].weekday())

        return context

    @staticmethod
    def get_month_days():
        today = localtime().date()
        year = today.year
        month = today.month

        first_day = date(year, month, 1)
        next_month = month % 12 + 1
        next_month_year = year if month < 12 else year + 1
        first_day_next_month = date(next_month_year, next_month, 1)
        last_day = first_day_next_month - timedelta(days=1)

        return [
            first_day + timedelta(days=i)
            for i in range((last_day - first_day).days + 1)
        ]
