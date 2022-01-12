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
        post_response = r.post(self.url, json=self.body)
        self.assertEqual(post_response.status_code, 201)
        get_response = r.get(self.url + str(next_id))
        self.assertEqual(get_response.status_code, 200)

    def test_name_processed(self):
        post_response = r.post(self.url, json=self.body)
        self.assertEqual(post_response.status_code, 201)
        get_response = r.get(self.url + str(self.body["id"])).json()
        self.assertEqual(self.body["name"], get_response["name"])

    def test_large_id(self):
        self.body["id"] = 9223372036854775807
        r.delete(self.url + str(self.body["id"]))
        post_response = r.post(self.url, json=self.body)
        self.assertEqual(post_response.status_code, 201)
        get_response = r.get(self.url + str(self.body["id"]))
        self.assertEqual(get_response.status_code, 200)

    def test_no_name(self):
        del(self.body["name"])
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_extra_field(self):
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

    def test_deny_negative_id_fails_gracefully(self):
        self.body["id"] = -1
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_overflow_id_fails_gracefully(self):
        self.body["id"] = 9223372036854775808
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_double_submission_fails_gracefully(self):
        r.post(self.url, json=self.body)
        response = r.post(self.url, json=self.body)
        self.assertEqual(response.status_code, 400)

