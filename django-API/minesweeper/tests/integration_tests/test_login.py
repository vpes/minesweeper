import datetime
import json

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from minesweeper.models.token import Token

class AuthAPITestCase(APITestCase):
    def setUp(self):
        def reset_token(user):
            token = Token.objects.filter(user=user)
            token = [t.delete() for t in token]
            token = Token.objects.create(user=user)

            return token.key
        self.user = get_user_model().objects.first()
        self.token = reset_token(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token {}".format(self.token)
            )

class LoginCase(AuthAPITestCase):
    def setUp(self):
        return

    def test_login_request(self):
        start_date = (
            (
                datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
                + datetime.timedelta(days=5)
            )
            .date()
            .strftime("%Y-%m-%d")
        )
        url = "http://localhost:8000/v1/login/"
        data = {"email": self.user.email, "password": self.user.password}
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
