"""
    DRF custom authentication class
"""
# coding: utf8
from django.utils.translation import ugettext_lazy as _

from rest_framework import authentication
from rest_framework import exceptions

from .models.token import Token


class CustomTokenAuthentication(authentication.TokenAuthentication):
    model = Token

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key, is_active=True)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                _('Invalid token: {}.'.format(key)), code=100)

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'), code=101)

        return (token.user, token)
