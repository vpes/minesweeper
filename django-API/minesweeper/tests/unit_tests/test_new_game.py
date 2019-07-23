import pytest
from minesweeper.factories.game import GameFactory

def test_new_game():
    game = GameFactory()