import django.urls

import preparation.views

app_name = "preparation"


urlpatterns = [
    django.urls.path(
        "",
        preparation.views.TestListView.as_view(),
        name="test_list",
    ),
    django.urls.path(
        "test/<int:pk>/",
        preparation.views.TaskView.as_view(),
        name="test",
    ),
    django.urls.path(
        "test/<int:test_id>/<int:pk>/",
        preparation.views.TaskDetailView.as_view(),
        name="task_detail",
    ),
    django.urls.path(
        "test/<int:test_id>/result/",
        preparation.views.TestResultView.as_view(),
        name="test_result",
    ),
]


__all__ = ()
