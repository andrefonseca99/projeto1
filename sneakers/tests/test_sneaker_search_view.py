from django.urls import resolve, reverse
from sneakers import views

from .test_sneaker_base import SneakerTestBase


class SneakerSearchViewTest(SneakerTestBase):

    def test_sneaker_search_view_function_is_correct(self):
        view = resolve(reverse('sneakers:search'))
        self.assertIs(view.func.view_class, views.SneakerListViewSearch)

    def test_sneaker_search_loads_correct_template(self):
        response = self.client.get(reverse('sneakers:search') + '?q=teste')
        self.assertTemplateUsed(response, 'sneakers/pages/search.html')

    def test_sneaker_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('sneakers:search'))
        self.assertEqual(response.status_code, 404)

    def test_sneaker_search_term_is_on_title_and_escaped(self):
        response = self.client.get(reverse('sneakers:search') + '?q=Teste')
        self.assertIn('Search for &quot;Teste &quot;| Sneakers', response.content.decode('utf-8'))  # noqa: E501

    def test_sneaker_search_can_find_sneaker_by_title(self):
        title1 = 'This is sneaker one'
        title2 = 'This is sneaker two'

        sneaker1 = self.make_sneaker(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        sneaker2 = self.make_sneaker(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('sneakers:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(sneaker1, response1.context['sneakers'])
        self.assertNotIn(sneaker2, response1.context['sneakers'])

        self.assertIn(sneaker2, response2.context['sneakers'])
        self.assertNotIn(sneaker1, response2.context['sneakers'])

        self.assertIn(sneaker1, response_both.context['sneakers'])
        self.assertIn(sneaker2, response_both.context['sneakers'])
