"""
    API URL endpoints
"""
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from minesweeper.api_v1.views.health_view import health_view
from minesweeper.api_v1.urls import (private_urlpatterns_v2, login_urlpatterns)

urlpatterns = [
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# Version API 1
urlpatterns_v1 = [
    path(
        'v1/', health_view
    ),
    path(
        'v1/', include(login_urlpatterns)
    ),
    path(
        'v1/', include(private_urlpatterns_v2)
    ),
]

urlpatterns += urlpatterns_v1

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
