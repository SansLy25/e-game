import django.urls

import preparation.views

app_name = "preparation"


urlpatterns = [
    django.urls.path(
        "<str:exam>/preparation/",
        preparation.views.PreparationListView.as_view(),
        name="exam_tasks",
    ),
    django.urls.path(
        "<str:exam>/preparation/task/<int:pk>/",
        preparation.views.TaskDetailView.as_view(),
        name="task_detail",
    ),
]


__all__ = ()
