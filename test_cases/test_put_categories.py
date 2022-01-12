import requests as r
from unittest import TestCase
from uuid import uuid4
from datetime import datetime
from random import randrange


class TestPostCategories(TestCase):

    def setUp(self):
        self.url = "http://localhost:8888/api/blog/categories/"
        self.headers = {"Accept": "application/json"}
        self.body = {"name": f"{uuid4()}_{datetime.now()}_put", "id": randrange(100, 199)}
        r.post(self.url, json=self.body)

    def tearDown(self):
        r.delete(self.url + str(self.body["id"]))

    def test_update_existing_category(self):
        update_body = {"name": f"{uuid4()}_{datetime.now()}"}
        put_response = r.put(self.url + str(self.body["id"]), json=update_body)
        self.assertEqual(put_response.status_code, 204)
        get_response = r.get(self.url + str(self.body["id"])).json()
        self.assertEqual(update_body["name"], get_response["name"])

    def test_update_non_existent_category(self):
        r.delete(self.url + str(self.body["id"]))
        put_response = r.put(self.url + str(self.body["id"]), json=self.body)
        self.assertEqual(put_response.status_code, 404)

    def test_large_id(self):
        large_id_body = {"name": f"{uuid4()}_{datetime.now()}_put", "id": 9223372036854775807}
        r.delete(self.url + str(large_id_body["id"]))
        r.post(self.url, json=large_id_body)
        update_body = {"name": f"{uuid4()}_{datetime.now()}"}
        put_response = r.put(self.url + str(large_id_body["id"]), json=update_body)
        self.assertEqual(put_response.status_code, 204)
        get_response = r.get(self.url + str(large_id_body["id"])).json()
        self.assertEqual(update_body["name"], get_response["name"])
        r.delete(self.url + str(large_id_body["id"]))

    def test_no_name(self):
        del(self.body["name"])
        put_response = r.put(self.url + str(self.body["id"]), json=self.body)
        self.assertEqual(put_response.status_code, 400)

    def test_extra_field(self):
        put_response = r.put(self.url + str(self.body["id"]),
                             json={"name": f"{uuid4()}_{datetime.now()}", "foo": "bar"})
        self.assertEqual(put_response.status_code, 204)

    def test_null_name(self):
        self.body["name"] = None
        put_response = r.put(self.url + str(self.body["id"]), json=self.body)
        self.assertEqual(put_response.status_code, 400)

    def test_non_english_characters(self):
        all_characters = r.get("https://bit.ly/3Fiee6W").content.decode("utf-8").strip("\n")
        self.body["name"] = all_characters
        response = r.put(self.url + str(self.body["id"]), json=self.body)
        self.assertEqual(response.status_code, 204)

    def test_large_name(self):
        large_name = r.get("https://bit.ly/3qdop8z").content.decode("utf-8").strip("\n")
        self.body["name"] = large_name
        response = r.put(self.url + str(self.body["id"]), json=self.body)
        self.assertEqual(response.status_code, 204)

    def test_overflow_id_fails_gracefully(self):
        self.body["id"] = 9223372036854775808
        response = r.put(self.url + str(self.body["id"]), json=self.body)
        self.assertEqual(response.status_code, 400)
