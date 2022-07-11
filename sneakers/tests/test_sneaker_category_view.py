from django.urls import resolve, reverse
from sneakers import views

from .test_sneaker_base import SneakerTestBase


class SneakerCategoryViewTest(SneakerTestBase):

    def test_sneaker_category_view_function_is_correct(self):
        view = resolve(reverse('sneakers:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertIs(view.func, views.category)

    def test_sneaker_category_view_return_404_if_no_sneakers_found(self):
        response = self.client.get(reverse('sneakers:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_sneaker_category_template_loads_sneakers(self):
        needed_title = 'This is a category text'
        # We need a sneaker for this test
        self.make_sneaker(title=needed_title)
        response = self.client.get(reverse('sneakers:category', kwargs={'category_id': 1}))  # noqa: E501
        content = response.content.decode('utf-8')
        # Check if one sneaker exists
        self.assertIn(needed_title, content)

    def test_sneaker_category_template_dont_load_sneakers_not_published(self):
        # We need a sneaker for this test
        sneaker = self.make_sneaker(is_published=False)
        response = self.client.get(reverse('sneakers:category', kwargs={'category_id': sneaker.category.id}))  # noqa: E501
        # Check if the sneaker will be found
        self.assertEqual(response.status_code, 404)
