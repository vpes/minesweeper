from django.conf.urls import url
from rest_framework import routers

from minesweeper.api_v1.views.game import GameViewSet
from minesweeper.api_v1.views.login import NativeLoginView


login_urlpatterns = [
    url(r'^login/$',
        NativeLoginView.as_view(),
        name="login"),

]


private_router = routers.DefaultRouter()
private_router.register(r"game/?", GameViewSet, basename="games")
private_urlpatterns_v2 = private_router.urls

