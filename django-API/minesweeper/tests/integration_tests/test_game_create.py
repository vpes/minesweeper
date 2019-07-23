
from .test_login import AuthAPITestCase


class GameCreateCase(AuthAPITestCase):

    def test_succesfull_create_request(self):
        url = "http://localhost:8000/v1/game/"
        response = self.client.post(url, data={"rows": 20,
                                               "columns": 20,
                                               "mines_count": 40})
        self.assertEqual(response.status_code, 201)
        self.assertIn("created", response.data[0])
