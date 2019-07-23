"""
    Mixins for Views of the stations application
"""
import django

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import get_authorization_header

from rest_framework.settings import api_settings

from minesweeper.authentications import CustomTokenAuthentication


class AuthException(object):

    status_code = 401
    default_detail = 'A server error ocurred.'

    def __init__(self, status=None, detail=None):
        self.status = status if status else self.status_code
        self.detail = detail if detail else self.default_detail

    def crash(self):
        return JsonResponse(
            {
                'status': 'error',
                'message': self.detail
            },
            status=self.status,
        )

class AuthTokenMixin(object):
    authentication_classes = (CustomTokenAuthentication,)

    def __init__(self, *args, **kwargs):
        super(AuthTokenMixin, self).__init__(*args, **kwargs)
        self.token = None
        self.user = None

    def authenticate_token(self):
        auth = get_authorization_header(self.request).split()

        if not auth or auth[0].lower() != b'token':
            exception = AuthException(
                detail='Missing or invalid authentication method.'
            )
            return (None, exception)

        if len(auth) == 1:
            exception = AuthException(
                detail='Invalid token header. No credentials provided.'
            )
            return (None, exception)

        if len(auth) > 2:
            exception = AuthException(
                detail='Invalid token header. Token string should not contain spaces.' # NOQA
            )
            return (None, exception)

        try:
            token = auth[1].decode()
        except UnicodeError:
            exception = AuthException(
                detail='Invalid token header. Token string should not contain invalid characters.' # NOQA
            )
            return (None, exception)

        return (token, None)

    def authenticate_credentials(self, key):
        from urbvan_core.models.token import Token
        try:
            token = Token.objects.select_related('user').get(key=key, is_active=True)
        except Token.DoesNotExist:
            exception = AuthException(detail=_('Invalid token.'))
            return (None, exception)

        if not token.user.is_active or token.user.is_removed:
            exception = AuthException(detail='User is not active or is removed.') # NOQA
            return (None, exception)

        if (token.expiration_date < timezone.now()):
            exception = AuthException(detail='Token has expired.') # NOQA
            token.is_active = False
            token.save()
            return (None, exception)
        token.reload_expiration_date()
        token.save()
        return (token, None)

    def dispatch(self, request, *args, **kwargs):
        key, token_exception = self.authenticate_token()
        if token_exception:
            return token_exception.crash()

        token, exception = self.authenticate_credentials(key)
        if exception:
            return exception.crash()

        self.token = token
        self.user = token.user
        return super(AuthTokenMixin, self).dispatch(request, *args, **kwargs) # NOQA


class UserSessionMixin:

    def retrieve_user(self, token, *args, **kwargs):
        user_class = django.contrib.auth.get_user_model()
        username = kwargs.get('username', None)
        uuid = kwargs.get('uuid', None)
        if username:
            try:
                user = user_class.objects.get(username=username)
            except user_class.DoesNotExist:
                user = None
        elif uuid:
            try:
                user = user_class.objects.get(uuid=uuid)
            except user_class.DoesNotExist:
                user = None
        else:
            return (token.user, None)

        if user != token.user:
            exception = AuthException(
                detail='Forbidden',
                status=403
            )
            return (None, exception)

        return (user, None)

    def dispatch(self, request, *args, **kwargs):
        user, user_exception = self.retrieve_user(token=self.token, *args, **kwargs) # NOQA
        if user_exception:
            return user_exception.crash()
        return super(UserSessionMixin, self).dispatch(request, *args, **kwargs)

class ValidateParamMixin:
    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def _validate_request_params(self, data, required_params):
        for param in required_params:
            if param in ['pk','client','user']:
                continue
            value = data.get(param)
            if value is None:
                error = "Missing parameter"
                error['detail'] = error['detail'].format(param)
                raise ValidationError(error['detail'],error['code'])
            setattr(self, param, value)
