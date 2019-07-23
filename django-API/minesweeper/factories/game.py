import factory
from factory.fuzzy import FuzzyInteger
from minesweeper.models.game import MS_Game
from minesweeper.factories.user import UserFactory


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MS_Game

    user = factory.SubFactory(UserFactory)
    rows = FuzzyInteger(4, 64)
    columns = FuzzyInteger(4, 64)
    mines_count = 4
