import datetime
import random

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_fsm import transition, FSMField

UserModel = get_user_model()


class MS_Game(models.Model):
    GAME_STATUS = (
        ("new", _("New")),
        ("started", _("Started")),
        ("paused", _("Paused")),
        ("won", _("Won")),
        ("lose", _("Lose")),
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = FSMField(default="new", choices=GAME_STATUS, db_index=True)
    rows = models.PositiveSmallIntegerField()
    columns = models.PositiveSmallIntegerField()
    mines_count = models.PositiveSmallIntegerField()
    mines = ArrayField(base_field=models.PositiveSmallIntegerField())
    board = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)
    ellapsed_time = models.TimeField(null=True)

    class Meta:
        managed = True
        db_table = "game"
        verbose_name = _("Game")
        verbose_name_plural = _("Games")

    def __str__(self):
        """Game name."""
        return "{}: {} ({:%Y-%m-%d %H:%M})".format(self.user, self.status, self.created)

    def __init__(
        self, user, rows: int, columns: int, mines_count: int, *args, **kwargs
    ):
        """
            A constructur with the basic attributes
        :param user: User of the game
        :param rows: width of the board
        :param columns: height of the board
        :param mine_count: Number of mines
        """
        super().__init__(*args, **kwargs)
        self.user = user
        self.rows = rows
        self.columns = columns
        if mines_count < 1 or mines_count > rows * columns - 1:
            raise Exception(_("Bad mines count argument"))
        self.mines_count = mines_count

    def _add_mines(self, mines_count: int, size: int, excluded: int):
        """
        Add <mines_count> random mines and store it into the mines array
        :param mines_count:number of mines
        :param size: height and width of the board
        :return:
        """
        self.mines = random.sample(range(size), mines_count)
        index = self.mines.index(excluded)
        if index >= 0:
            new_value = random.randint(size)
            while new_value in self.mines:
                new_value = random.randint(size)
            self.mines[index] = new_value


    def _create_board(self, rows: int, columns: int):
        """
        Crewates the board matrix using the given rows and columns
        :param rows: Integer > 0
        :param columns: Integer > 0
        :return:
        """
        board = []
        sorted_mines = sorted(self.mines)
        for i in range(rows):
            row = []
            for j in range(columns):
                has_bomb = sorted_mines.index(i * columns + j)
                row.append({"c": j+1, # c column number base 1
                            "r": i+1, # r row number base 1
                            "v": False, # v visible
                            "f": False, # f flag
                            "n": 0 if has_bomb else self.calculate_neighbors(i,j), # n neighbors value
                            "b":  has_bomb# has a bomb
                            })
            board.append(row)
        self.board = {"board": board}

    def toggle_red_flag(self, row: int, column: int):
        self.board[row][column]["f"] = not self.board[row][column]["f"]

    def cell_visible(self, row: int, column: int):
        cell = self.board[row][column]
        if self.status == 'new':
            self.start(row, column)
        if cell["b"]: # Has bomb
            self.loose()
        elif not cell["v"]:
            cell["v"] = True
        self.save()

    def calculate_neighbors(self, row, column):
        pass

    # Finite State Machine methods
    @transition(field=status, source="new", target="started")
    def start(self, row, column, **kwargs):
        self._add_mines(self.mines_count, self.rows * self.columns, row * self.rows + column)
        self._create_board(self.rows, self.columns)
        self.started = datetime.datetime.now()

    @transition(field=status, source="started", target="lose")
    def loose(self, **kwargs):
        self.ended = datetime.datetime.now()

    @transition(field=status, source="started", target="won")
    def win(self, **kwargs):
        self.ended = datetime.datetime.now()

    @transition(field=status, source="started", target="paused")
    def pause(self, **kwargs):
        pass

    @transition(field=status, source="paused", target="started")
    def resume(self, **kwargs):
        pass
