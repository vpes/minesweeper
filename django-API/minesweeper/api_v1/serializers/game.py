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
    #Commented for debugging
    board = serializers.SerializerMethodField()
    class Meta:
        model = MS_Game
        fields = ("id", "board", "started", "status")

    def get_board(self, obj):
        result = []
        for row in obj.board:
            result_row = []
            for cell in row:
                result_row.append({"f": cell["f"],
                                   "v": cell["v"],
                                   "n": cell["n"] if cell["v"] else None})
            result.append(result_row)
        return result