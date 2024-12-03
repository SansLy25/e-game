from django.urls import path

import homepage.views

urlpatterns = [
    path("", homepage.views.HomePageView.as_view(), name="home"),
]
