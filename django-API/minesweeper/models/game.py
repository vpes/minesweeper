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
        ("win", _("Win")),
        ("lose", _("Lose")),
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = FSMField(default="new", choices=GAME_STATUS, db_index=True)
    size = models.PositiveSmallIntegerField()
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
        super(models.Model, self).__init__(self, *args, **kwargs)
        self.user = user
        self.rows = rows
        self.columns = columns
        self._add_mines(mines_count, rows * columns)
        self._create_board(rows, columns)

    def _add_mines(self, mines_count: int, size: int):
        """
        Add <mines_count> random mines and store it into the mines array
        :param mines_count:number of mines
        :param size: height and width of the board
        :return:
        """
        if mines_count < 1 or mines_count > size - 1:
            raise Exception(_("Bad mines count argument"))
        self.mines = random.sample(range(size), mines_count)

    def _create_board(self, rows: int, columns: int):
        """
        Crewates the board matrix using the given rows and columns
        :param rows: Integer > 0
        :param columns: Integer > 0
        :return:
        """
        board = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append({"c": j+1, "r": i+1, "s": False, "m": False})
            board.append(row)
        self.board = {"board": board}
