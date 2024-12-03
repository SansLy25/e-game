from django.conf.urls.static import static
from django.contrib import admin
import django.urls
from django.urls import include, path

from egame import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
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
