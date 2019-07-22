"""
    API URL endpoints
"""
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from minesweeper.views.health_view import health_view

urlpatterns = [
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# Version API 1
urlpatterns_v1 = [
    path(
        '', health_view
    ),
]

urlpatterns += urlpatterns_v1

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
