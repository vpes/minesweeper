"""
    Creation and play test
"""
import random

import pytest
from minesweeper.factories.game import GameFactory


def test_new_game():
    """
        Random rows an columns game creation test
    """
    game = GameFactory()
    rows = game.rows
    columns = game.columns
    assert len(game.board) == rows and len(game.board[0]) == columns

def test_start_game():
    """
        Start game test
    """
    game = GameFactory()
    row = random.randint(0, game.rows - 1)
    column = random.randint(0, game.columns - 1)
    game.select_cell(row, column)
    # Status change
    assert game.status == "started"
    # Visibility change
    assert game.board[row][column]["v"] == True
    # Mines count
    mines = 0
    for i in range(game.rows):
        for j in range(game.columns):
            if game.board[i][j]["b"]:
                mines += 1
    assert mines == 40
    row = game.mines[0] // game.columns
    column = game.mines[0] % game.columns
    assert game.board[row][column]["b"] == True
    game.select_cell(row, column)
    assert game.status == "lose"
