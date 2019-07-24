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
    mines = ArrayField(base_field=models.PositiveSmallIntegerField(), null=True)
    flags = ArrayField(base_field=models.PositiveSmallIntegerField(), null=True)
    discovered_cells = models.PositiveSmallIntegerField(default=0)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            if (
                self.rows < 3
                or self.columns < 3
                or self.rows > 1000
                or self.columns > 1000
            ):
                raise Exception(_("Bad board size (min 3, max 1000)"))
            if self.mines_count < 1 or self.mines_count > (self.rows * self.columns) / 2:
                raise Exception(_("Bad mines count argument"))
            self._create_board()
        super(MS_Game, self).save(*args, **kwargs)

    def _create_board(self):
        """
        Crewates the board matrix using the given rows and columns
        :param rows: Integer > 0
        :param columns: Integer > 0
        :return:
        """
        board = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(
                    {
                        "c": j + 1,  # c column number base 1
                        "r": i + 1,  # r row number base 1
                        "v": False,  # v visible
                        "f": 0,  # f flag
                        "n": 0,  # n neighbors value
                        "b": False,  # has a bomb , The bombs are created on start
                    }
                )
            board.append(row)
        self.board = board

    def _add_mines(self, mines_count: int, size: int, excluded: int):
        """
        Add <mines_count> random mines and store it into the mines array
        :param mines_count:number of mines
        :param size: height and width of the board
        :return:
        """
        self.mines = random.sample(range(size), mines_count)
        excluded_list = [excluded]
        not_is_left = excluded % self.columns > 0
        not_is_rigth = excluded % self.columns < self.columns - 1
        if excluded // self.rows > 0:
            if not_is_left:
                excluded_list.append(excluded - self.columns - 1)
            excluded_list.append(excluded - self.columns)
            if not_is_rigth:
                excluded_list.append(excluded - self.columns + 1)
        if not_is_left:
            excluded_list.append(excluded - 1)
        if not_is_rigth:
            excluded_list.append(excluded + 1)
        if excluded // self.rows < self.rows - 1:
            if not_is_left:
                excluded_list.append(excluded + self.columns - 1)
            excluded_list.append(excluded + self.columns)
            if not_is_rigth:
                excluded_list.append(excluded + self.columns + 1)
        for el in excluded_list:
            try:
                index = self.mines.index(el)
                if index >= 0:
                    new_value = random.randint(0, size - 1)
                    while new_value in self.mines or new_value in excluded_list:
                        new_value = random.randint(0, size - 1)
                    self.mines[index] = new_value
            except ValueError:
                # index method throws ValueError exception if the value is not in the list
                pass
        for mine in self.mines:
            row = mine // self.columns
            column = mine % self.columns
            self._add_bomb(row, column)

    def _add_bomb(self, row, column):
        cell = self.board[row][column]
        cell["b"] = True
        self._calculate_neighbors(row, column)

    def _calculate_neighbors(self, row, column):
        if row > 0:
            if column > 0:
                self.board[row - 1][column - 1]["n"] += 1
            self.board[row - 1][column]["n"] += 1
            if column < self.columns - 1:
                self.board[row - 1][column + 1]["n"] += 1
        if column > 0:
            self.board[row][column - 1]["n"] += 1
        if column < self.columns - 1:
            self.board[row][column + 1]["n"] += 1
        if row < self.rows - 1:
            if column > 0:
                self.board[row + 1][column - 1]["n"] += 1
            self.board[row + 1][column]["n"] += 1
            if column < self.columns - 1:
                self.board[row + 1][column + 1]["n"] += 1

    def toggle_flag(self, row: int, column: int):
        """
            Toggle the flags value between 3 states
            0: Not flag
            1: Flag
            2: Conditional flag
        :param row:
        :param column:
        :return:
        """
        if self.flags is None:
            self.flags = []
        cell = self.board[row][column]
        flag_pos = row * self.columns + column
        if cell["f"] == 1:
            self.flags.pop(self.flags.index(flag_pos))
        elif cell["f"] == 0:
            self.flags.append(flag_pos)
        cell["f"] = (cell["f"] + 1) % 3
        self.save()
        return cell["f"], len(self.flags)

    def select_cell(self, row: int, column: int):
        result = None
        if self.status == "new":
            self.start(row, column)
        cell = self.board[row][column]
        if cell["b"]:  # Has bomb
            result = [(row, column, -1)]
            self.loose()
        elif not cell["v"]:
            result = self._connected_empty_cells(row, column)
            self.discovered_cells += len(result)
        self.save()
        return result

    def _connected_empty_cells(self, row: int, column: int):
        cell = self.board[row][column]
        result = []
        if not (cell["v"] or cell["b"]):
            cell["v"] = True
            result.append((row, column, cell["n"]))
            if cell["n"] == 0:
                if row > 0:
                    if column > 0:
                        result += self._connected_empty_cells(row - 1, column - 1)
                    result += self._connected_empty_cells(row - 1, column)
                    if column < self.columns - 1:
                        result += self._connected_empty_cells(row - 1, column + 1)
                if column > 0:
                    result += self._connected_empty_cells(row, column - 1)
                if column < self.columns - 1:
                    result += self._connected_empty_cells(row, column + 1)
                if row < self.rows - 1:
                    if column > 0:
                        result += self._connected_empty_cells(row + 1, column - 1)
                    result += self._connected_empty_cells(row + 1, column)
                    if column < self.columns - 1:
                        result += self._connected_empty_cells(row + 1, column + 1)
        return result

    # Finite State Machine methods
    @transition(field=status, source="new", target="started")
    def start(self, row, column, **kwargs):
        self._add_mines(
            self.mines_count, self.rows * self.columns, row * self.rows + column
        )
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
