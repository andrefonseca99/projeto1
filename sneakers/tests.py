from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class SneakerURLsTest(TestCase):

    def test_sneakers_home_url_is_correct(self):
        url = reverse('sneakers:home')
        self.assertEqual(url, '/')

    def test_sneakers_category_url_is_correct(self):
        url = reverse('sneakers:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/sneakers/category/1/')

    def test_sneakers_sneakers_url_is_correct(self):
        url = reverse('sneakers:sneaker', kwargs={'id': 1})
        self.assertEqual(url, '/sneakers/1/')
