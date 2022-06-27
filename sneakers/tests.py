from django.test import TestCase
from django.urls import resolve, reverse

from sneakers import views

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


class SneakerViewsTest(TestCase):

    def test_sneaker_home_view_function_is_correct(self):
        view = resolve(reverse('sneakers:home'))
        self.assertIs(view.func, views.home)

    def test_sneaker_category_view_function_is_correct(self):
        view = resolve(reverse('sneakers:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_sneaker_detail_view_function_is_correct(self):
        view = resolve(reverse('sneakers:sneaker', kwargs={'id': 1}))
        self.assertIs(view.func, views.sneaker)
