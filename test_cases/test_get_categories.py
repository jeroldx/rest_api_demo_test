import requests as r
from unittest import TestCase
from uuid import uuid4
from datetime import datetime
from random import randrange


class TestGetCategories(TestCase):

    def setUp(self):
        self.url = "http://localhost:8888/api/blog/categories/"
        self.headers = {"Accept": "application/json"}

    def test_up(self):
        self.assertEqual(r.options(self.url).status_code, 200)

    def test_returns_list(self):
        self.assertIsInstance(r.get(self.url).json(), list)

    def test_displays_all_categories(self):
        min_categories = 5
        submitted_ids = []
        for i in range(min_categories):
            category_id = randrange(100, 199)
            submitted_ids.append(category_id)
            r.post(self.url, json={"name": f"{uuid4()}_{datetime.now()}_get", "id": category_id})
        self.assertGreaterEqual(len(r.get(self.url).json()), min_categories)
