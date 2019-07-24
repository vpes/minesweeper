import json

from .test_login import AuthAPITestCase


class GameCreateCase(AuthAPITestCase):
    def test_succesfull_create_request(self):
        url = "http://localhost:8000/v1/game/"
        response = self.client.post(
            url,
            data=json.dumps({"rows": 20, "columns": 20, "mines_count": 40}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual("new", response.data["status"])

    def test_select_cell_request(self):
        url = "http://localhost:8000/v1/game/"
        response = self.client.post(
            url,
            data=json.dumps({"rows": 20, "columns": 20, "mines_count": 40}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual("new", response.data["status"])
        url = "http://localhost:8000/v1/game/{}/select_cell/".format(response.data["id"])
        response = self.client.post(
            url,
            data=json.dumps({"row": 10, "col": 4}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
