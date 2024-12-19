from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.urls
import django.urls
from django.urls import include, path

import homepage.urls
import leaderboard.urls
import planning.urls
import practice.urls
import preparation.urls
import statistic.urls
import users.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(homepage.urls, namespace="homepage")),
    path("", include(users.urls, namespace="users")),
    path("", include(django.contrib.auth.urls)),
    path("planning/", include(planning.urls, namespace="planning")),
    path("api/practice/", include(practice.urls, namespace="api_practice")),
    path("api/statistic/", include(statistic.urls, namespace="api_statistic")),
    path(
        "<slug:exam_slug>/practice/",
        include(practice.urls, namespace="practice"),
    ),
    path(
        "<slug:exam_slug>/statistic/",
        include(statistic.urls, namespace="statistic"),
    ),
    path("<slug:exam_slug>/preparation/", include(preparation.urls)),
    path("leaderboard/", include(leaderboard.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0],
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path("__debug/", django.urls.include(debug_toolbar.urls)),
    )
