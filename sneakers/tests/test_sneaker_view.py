from django.test import TestCase
from django.urls import resolve, reverse
from sneakers import views
from sneakers.models import Category, Sneaker, User

# Create your tests here.


class SneakerViewsTest(TestCase):

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
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        sneaker = Sneaker.objects.create(
            category=category,
            author=author,
            title='Sneaker Title',
            description='Sneaker Description',
            slug='sneaker-slug',
            condition_value=10,
            condition_unit='/10',
            price=100,
            price_unit='R$',
            sneaker_description='Sneaker condition description',
            sneaker_description_is_html=False,
            is_published=True,
            cover='media\\sneakers\\covers\2022\06\15\\WhatsApp_Image_2022-06-15_at_11.24.14.jpeg'  # noqa: E501
        )

        sneaker = sneaker
        response = self.client.get(reverse('sneakers:home'))
        content = response.content.decode('utf-8')
        response_context_sneakers = response.context['sneakers']
        self.assertIn('Sneaker Title', content)
        self.assertIn('Sneaker Description', content)
        self.assertIn('10/10', content)
        self.assertIn('R$ 100', content)
        self.assertEqual(len(response_context_sneakers), 1)

    def test_sneaker_category_view_function_is_correct(self):
        view = resolve(reverse('sneakers:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertIs(view.func, views.category)

    def test_sneaker_category_view_return_404_if_no_sneakers_found(self):
        response = self.client.get(reverse('sneakers:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_sneaker_detail_view_function_is_correct(self):
        view = resolve(reverse('sneakers:sneaker', kwargs={'id': 1000}))
        self.assertIs(view.func, views.sneaker)

    def test_sneaker_detail_view_return_404_if_no_sneakers_found(self):
        response = self.client.get(reverse('sneakers:sneaker', kwargs={'id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)
