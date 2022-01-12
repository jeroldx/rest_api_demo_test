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
        self.body = {"name": f"{uuid4()}_{datetime.now()}_get_blog", "id": self.category_id}
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

    def test_get_category_no_posts(self):
        r.post(self.url, json=self.body)
        get_response = r.get(self.url + str(self.body["id"]))
        self.assertEqual(get_response.status_code, 200)

    def test_get_category_with_post(self):
        r.post(self.url, json=self.body)
        r.post(self.blog_url, json=self.blog_body)
        get_response = r.get(self.url + str(self.body["id"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.json()["posts"]), 1)

    def test_get_non_existent_category(self):
        get_response = r.get(self.url + str(self.body["id"]))
        self.assertEqual(get_response.status_code, 404)
