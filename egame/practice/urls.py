from django.urls import path

import practice.views

urlpatterns = [
    path(
        "",
        practice.views.VariantCreationView.as_view(),
        name="variant_creation",
    ),
    path(
        "<int:variant_id>/",
        practice.views.VariantSolutionView.as_view(),
        name="variant_solution",
    ),
    path(
        "get_solution/<int:variant_id>/<int:task_id>/",
        practice.views.GetSolutionAPIView.as_view(),
        name="get_solution",
    ),
]
