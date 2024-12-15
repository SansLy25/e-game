from django.urls import path

import statistic.views

app_name = "statistic"

urlpatterns = [
    path(
        "get_exam_statistic/<slug:exam_slug>/",
        statistic.views.GetExamStatisticAPIView.as_view(),
        name="get_exam_statistic",
    ),
    path(
        "",
        statistic.views.ExamStatisticView.as_view(),
        name="exam_statistic",
    ),
]
