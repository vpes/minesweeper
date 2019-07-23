# coding: utf8
import types

from django.conf import settings

from marshmallow import (Schema, fields, pre_dump)
from minesweeper.models.token import Token
from minesweeper.api_v1.views.utils import reset_token


class UserSchema(Schema):

    username = fields.String()
    email = fields.String()
    token = fields.String()

    first_name = fields.String()
    last_name = fields.String()


    @pre_dump
    def set_token(self, obj):
        token = getattr(obj, 'token', None)

        if not token:
            try:
                token = Token.objects.get(user=obj)
            except Exception:
                token = reset_token(obj)
                setattr(obj, 'token', token)
            else:
                setattr(obj, 'token', token.key)
        return obj

    @pre_dump
    def set_email(self, obj):
        obj.email = obj.email if obj.email is not None else ''
        return obj


class ResetPasswordSchema(Schema):

    uuid = fields.UUID()
    message = fields.String()
    success = fields.Boolean()
    seconds_to_expire = fields.Integer()
