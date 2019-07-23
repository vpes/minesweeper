# coding: utf8
import random

from django.contrib.auth import get_user_model
from minesweeper.models.token import Token


def random_digits(digits=1):
    """Retun random digits."""
    return str(int(random.random() * (10**digits)))


def generate_username(username=None, digits=1):
    """Generate unique usename."""
    if username:
        q = get_user_model().objects.filter(username=username).exists()
    else:
        raise Exception("username was not created")

    if q:
        username += random_digits(digits)
        return generate_username(
            username=username,
            digits=digits + 1
        )
    else:
        return username


def reset_token(user):

    token = Token.objects.filter(user=user)
    token = [t.delete() for t in token]
    token = Token.objects.create(user=user)

    return token.key

