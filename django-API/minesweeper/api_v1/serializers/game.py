"""
    Game Serializer
"""

from rest_framework import serializers

from minesweeper.models.game import MS_Game


class GameListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MS_Game
        fields = ("id", "status", "started", "ended")


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = MS_Game
        fields = ("id", "board", "started", "status")
