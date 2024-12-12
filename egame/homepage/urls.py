from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path("", homepage.views.HomePageView.as_view(), name="home"),
    path(
        "<slug:exam_slug>",
        homepage.views.ExamHomePageView.as_view(),
        name="exam_home",
    ),
]
