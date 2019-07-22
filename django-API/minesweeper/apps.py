from django.apps import AppConfig


class MinesweeperConfig(AppConfig):
    name = "minesweeper"

    def ready(self):
        from .models import (
            game,
            user,
            token
        )
