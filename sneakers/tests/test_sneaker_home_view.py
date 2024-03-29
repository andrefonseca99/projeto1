from unittest.mock import patch

from django.urls import resolve, reverse
from sneakers import views

from .test_sneaker_base import SneakerTestBase


class SneakerHomeViewTest(SneakerTestBase):

    def test_sneaker_home_view_function_is_correct(self):
        view = resolve(reverse('sneakers:home'))
        self.assertIs(view.func.view_class, views.SneakerListViewHome)

    def test_sneaker_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('sneakers:home'))
        self.assertEqual(response.status_code, 200)

    def test_sneaker_home_view_loads_correct_template(self):
        response = self.client.get(reverse('sneakers:home'))
        self.assertTemplateUsed(response, 'sneakers/pages/home.html')

    def test_sneaker_home_shows_no_sneakers_found_if_no_sneakers(self):
        response = self.client.get(reverse('sneakers:home'))
        self.assertIn('No sneakers found', response.content.decode('utf-8'))

    def test_sneaker_home_template_loads_sneakers(self):
        # Sneaker needed for this test
        self.make_sneaker()
        response = self.client.get(reverse('sneakers:home'))
        content = response.content.decode('utf-8')
        response_context_sneakers = response.context['sneakers']
        # Check if one sneaker exists
        self.assertIn('Sneaker Title', content)
        self.assertEqual(len(response_context_sneakers), 1)

    def test_sneaker_home_template_dont_load_sneakers_not_published(self):
        # Sneaker needed for this test
        self.make_sneaker(is_published=False)
        response = self.client.get(reverse('sneakers:home'))
        # Check if the sneaker will be found
        self.assertIn('No sneakers found', response.content.decode('utf-8'))

    def test_sneaker_home_is_paginated(self):

        self.make_sneaker_in_batch(qtd=8)

        with patch('sneakers.views.site.PER_PAGE', new=3):
            response = self.client.get(reverse('sneakers:home'))
            sneakers = response.context['sneakers']
            paginator = sneakers.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        # Creating 8 different sneakers for this test
        self.make_sneaker_in_batch(qtd=8)

        # Making PER_PAGE equals 3 to have 3 pages
        with patch('sneakers.views.site.PER_PAGE', new=3):
            response = self.client.get(reverse('sneakers:home') + '?page=1A')
            self.assertEqual(response.context['sneakers'].number, 1)

            response = self.client.get(reverse('sneakers:home') + '?page=2')
            self.assertEqual(response.context['sneakers'].number, 2)
