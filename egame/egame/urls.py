from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

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
