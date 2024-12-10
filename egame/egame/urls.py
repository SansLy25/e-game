from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.urls
import django.urls
from django.urls import include, path

import homepage.urls
import practice.urls
import users.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(homepage.urls)),
    path("", include(users.urls, namespace="users")),
    path("", include(django.contrib.auth.urls)),
    path("api/practice/", include(practice.urls)),
    path("<slug:exam_slug>/practice/", include(practice.urls)),
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

__all__ = ()
