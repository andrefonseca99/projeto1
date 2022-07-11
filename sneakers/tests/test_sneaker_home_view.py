from django.urls import resolve, reverse
from sneakers import views

from .test_sneaker_base import SneakerTestBase


class SneakerHomeViewTest(SneakerTestBase):

    def test_sneaker_home_view_function_is_correct(self):
        view = resolve(reverse('sneakers:home'))
        self.assertIs(view.func, views.home)

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
        # We need a sneaker for this test
        self.make_sneaker()
        response = self.client.get(reverse('sneakers:home'))
        content = response.content.decode('utf-8')
        response_context_sneakers = response.context['sneakers']
        # Check if one sneaker exists
        self.assertIn('Sneaker Title', content)
        self.assertEqual(len(response_context_sneakers), 1)

    def test_sneaker_home_template_dont_load_sneakers_not_published(self):
        # We need a sneaker for this test
        self.make_sneaker(is_published=False)
        response = self.client.get(reverse('sneakers:home'))
        # Check if the sneaker will be found
        self.assertIn('No sneakers found', response.content.decode('utf-8'))
