from django.urls import path

import planning.views

app_name = "planning"

urlpatterns = [
    path(
        "editing/",
        planning.views.ScheduleEditingView.as_view(),
        name="editing",
    ),
    path(
        "visiting/",
        planning.views.VisitingView.as_view(),
        name="visiting",
    ),
]
