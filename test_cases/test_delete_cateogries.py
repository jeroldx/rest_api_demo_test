import requests as r
from unittest import TestCase
from uuid import uuid4
from datetime import datetime
from random import randrange


class TestPostCategories(TestCase):

    def setUp(self):
        self.url = "http://localhost:8888/api/blog/categories/"
        self.blog_url = "http://localhost:8888/api/blog/posts/"
        self.headers = {"Accept": "application/json"}
        self.category_id = randrange(100, 199)
        self.body = {"name": f"{uuid4()}_{datetime.now()}_delete", "id": self.category_id}
        self.blog_body = {"body": f"{uuid4()}_{datetime.now()}",
                          "category_id": self.category_id,
                          "title": f"{uuid4()}_{datetime.now()}"}
        get_posts_response = r.get(self.url + str(self.body["id"])).json()
        if "posts" in get_posts_response:
            post_ids = [p["id"] for p in get_posts_response["posts"]]
            for post_id in post_ids:
                r.delete(self.blog_url + str(post_id))
        r.delete(self.url + str(self.body["id"]))

    def tearDown(self):
        get_posts_response = r.get(self.url + str(self.body["id"])).json()
        if "posts" in get_posts_response:
            post_ids = [p["id"] for p in get_posts_response["posts"]]
            for post_id in post_ids:
                r.delete(self.blog_url + str(post_id))
        r.delete(self.url + str(self.body["id"]))

    def test_delete_category(self):
        r.post(self.url, json=self.body)
        delete_response = r.delete(self.url + str(self.body["id"]))
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(r.get(self.url + str(self.body["id"])).status_code, 404)

    def test_delete_category_not_found(self):
        delete_response = r.delete(self.url + str(self.body["id"]))
        self.assertEqual(delete_response.status_code, 404)

    def test_delete_category_in_use(self):
        r.post(self.url, json=self.body)
        r.post(self.blog_url, json=self.blog_body)
        delete_response = r.delete(self.url + str(self.body["id"]))
        self.assertEqual(delete_response.status_code, 409)
        self.assertEqual(r.get(self.url + str(self.body["id"])).status_code, 200)

    def test_delete_after_removing_posts(self):
        r.post(self.url, json=self.body)
        r.post(self.blog_url, json=self.blog_body)
        post_ids = [p["id"] for p in r.get(self.url + str(self.body["id"])).json()["posts"]]
        for post_id in post_ids:
            r.delete(self.blog_url + str(post_id))
        delete_response = r.delete(self.url + str(self.body["id"]))
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(r.get(self.url + str(self.body["id"])).status_code, 404)

    def test_delete_overflow_value(self):
        self.body["id"] = 9223372036854775808
        delete_response = r.delete(self.url + str(self.body["id"]))
        self.assertEqual(delete_response.status_code, 400)
