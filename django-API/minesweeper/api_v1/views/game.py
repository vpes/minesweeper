
from rest_framework import generics, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .mixins import (
    AuthTokenMixin,
    UserSessionMixin,
    ValidateParamMixin,
)

from minesweeper.models.game import MS_Game
from minesweeper.api_v1.serializers.game import (GameSerializer, GameListSerializer)

class GameViewSet(
    AuthTokenMixin, UserSessionMixin, ValidateParamMixin, viewsets.ViewSet
):
    queryset = MS_Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request):
        required_params = [
            "rows",
            "columns",
            "mine_count",
        ]
        self._validate_request_params(request.data, required_params)
        game = MS_Game(self.user,
                    rows=self.rows,
                    columns=self.columns,
                    mine_count=self.mine_count)

        serializer = self.serializer_class(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            game = self.queryset.get(pk=pk, user_id=self.user.id)
            serializer = self.serializer_class(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MS_Game.DoesNotExist:
            return Response("The game does not exist", status=404)

    def list(self, request, *args, **kwargs):
        games = self.queryset.get(user_id=self.user.id).order_by("-created")
        serializer = GameListSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def select_cell(self, request, pk):
        required_params = [
            "row",
            "col",
        ]
        self._validate_request_params(request.data, required_params)
        game = self.queryset.get(pk=pk, user_id=self.user.id)
        game.select_cell(self.row, self.col)
        response = {}
        return Response(response, status=status.HTTP_200_OK)
