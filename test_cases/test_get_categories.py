import requests as r
from unittest import TestCase


class TestGetCategories(TestCase):

    def setUp(self):
        self.url = "http://localhost:8888/api/blog/categories/"
        self.headers = {"Accept": "application/json"}

    def test_up(self):
        self.assertEqual(r.options(self.url).status_code, 200)

    def test_returns_list(self):
        self.assertIsInstance(r.get(self.url).json(), list)
