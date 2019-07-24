from rest_framework import generics, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .mixins import AuthTokenMixin, UserSessionMixin, ValidateParamMixin

from minesweeper.models.game import MS_Game
from minesweeper.api_v1.serializers.game import GameSerializer, GameListSerializer


class GameViewSet(
    AuthTokenMixin, UserSessionMixin, ValidateParamMixin, viewsets.ViewSet
):
    queryset = MS_Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request):
        required_params = ["rows", "columns", "mines_count"]
        self._validate_request_params(request.data, required_params)
        game = MS_Game.objects.filter(
            user=self.user, status__in=["new", "started", "paused"]
        ).first()
        if game is None:
            game = MS_Game.objects.create(
                user=self.user,
                rows=int(self.rows),
                columns=int(self.columns),
                mines_count=int(self.mines_count),
            )
        serializer = self.serializer_class(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        required_params = ["row", "col"]
        self._validate_request_params(request.data, required_params)
        game = self.queryset.get(pk=pk, user_id=self.user.id)
        changed_cells = game.select_cell(self.row, self.col)
        response = {"cells": changed_cells}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def toggle_flag(self, request, pk):
        required_params = ["row", "col"]
        self._validate_request_params(request.data, required_params)
        game = self.queryset.get(pk=pk, user_id=self.user.id)
        flag, flag_count = game.toggle_flag(self.row, self.col)
        response = {"flag": flag, "flag_count": flag_count}
        return Response(response, status=status.HTTP_200_OK)
