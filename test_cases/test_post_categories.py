import requests as r
from unittest import TestCase
from uuid import uuid4
from datetime import datetime
from random import randrange


class TestPostCategories(TestCase):

    def setUp(self):
        self.url = "http://localhost:8888/api/blog/categories/"
        self.headers = {"Accept": "application/json"}
        self.body = {"name": f"{uuid4()}_{datetime.now()}", "id": randrange(100, 199)}
        r.delete(self.url + str(self.body["id"]))

    def tearDown(self):
        r.delete(self.url + str(self.body["id"]))

    def test_up(self):
        self.assertEqual(r.options(self.url).status_code, 200)

    def test_can_submit(self):
        self.assertEqual(r.post(self.url, json=self.body).status_code, 201)

    def test_id_incremented(self):
        get_response = r.get(self.url).json()
        id_list = [c["id"] for c in get_response if c["id"] >= 0]
        next_id = max(id_list) + 1 if len(id_list) > 0 else 0
        self.body["id"] = 0
        r.post(self.url, json=self.body)
        get_response = r.get(self.url).json()
        id_list = [c["id"] for c in get_response]
        self.assertIn(next_id, id_list)

    def test_submission_processed(self):
        r.post(self.url, json=self.body)
        get_response = r.get(self.url).json()
        self.assertIn(self.body["name"], [category["name"] for category in get_response])

    def test_large_id(self):
        self.body["id"] = 9223372036854775807
        r.delete(self.url + str(self.body["id"]))
        r.post(self.url, json=self.body)
        get_response = r.get(self.url).json()
        self.assertIn(self.body["id"], [category["id"] for category in get_response])

    def test_no_name(self):
        del(self.body["name"])
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_extra_fields(self):
        self.body["foo"] = "bar"
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 201)

    def test_null_name(self):
        self.body["name"] = None
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_non_english_characters(self):
        all_characters = r.get("https://bit.ly/3Fiee6W").content.decode("utf-8").strip("\n")
        self.body["name"] = all_characters
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 201)

    def test_large_name(self):
        large_name = r.get("https://bit.ly/3qdop8z").content.decode("utf-8").strip("\n")
        self.body["name"] = large_name
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 201)

    # Assuming these should fail gracefully with a 400 status
    def test_negative_id(self):
        self.body["id"] = -1
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_overflow_id(self):
        self.body["id"] = 9223372036854775808
        r.delete(self.url + str(self.body["id"]))
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_double_submission(self):
        r.post(self.url, json=self.body)
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

