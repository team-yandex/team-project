from django.test import Client, TestCase
from django.urls import reverse


class InfoTests(TestCase):
    """testing homepage & about"""

    def test_homepage(self):
        status = Client().get(reverse('info:index_page')).status_code
        self.assertEqual(status, 200)

    def test_about(self):
        status = Client().get(reverse('info:about_page')).status_code
        self.assertEqual(status, 200)
