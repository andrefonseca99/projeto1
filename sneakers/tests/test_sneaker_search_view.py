from django.urls import resolve, reverse
from sneakers import views

from .test_sneaker_base import SneakerTestBase


class SneakerSearchViewTest(SneakerTestBase):

    def test_sneaker_search_view_function_is_correct(self):
        view = resolve(reverse('sneakers:search'))
        self.assertIs(view.func, views.search)

    def test_sneaker_search_loads_correct_template(self):
        response = self.client.get(reverse('sneakers:search') + '?q=teste')
        self.assertTemplateUsed(response, 'sneakers/pages/search.html')

    def test_sneaker_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('sneakers:search'))
        self.assertEqual(response.status_code, 404)

    def test_sneaker_search_term_is_on_title_and_escaped(self):
        response = self.client.get(reverse('sneakers:search') + '?q=Teste')
        self.assertIn('Search for &quot;Teste &quot;| Sneakers', response.content.decode('utf-8'))  # noqa: E501
