from django.urls import path
import practice.views

urlpatterns = [
    path(
        "creation/",
        practice.views.VariantCreationView.as_view(),
        name="variant_creation",
    ),
    path(
        "solution/<int:variant_id>/",
        practice.views.VariantSolutionView.as_view(),
        name="variant_solution",
    ),
]
