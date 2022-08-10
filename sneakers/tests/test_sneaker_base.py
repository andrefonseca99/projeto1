from django.test import TestCase
from sneakers.models import Category, Sneaker, User


class SneakerMixin:

    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_sneaker(
        self,
        category_data=None,
        author_data=None,
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
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}
        return Sneaker.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            condition_value=condition_value,
            condition_unit=condition_unit,
            price=price,
            price_unit=price_unit,
            sneaker_description=sneaker_description,
            sneaker_description_is_html=sneaker_description_is_html,
            is_published=is_published,
            cover=cover
        )

    def make_sneaker_in_batch(self, qtd=10):
        sneakers = []
        for i in range(qtd):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            sneaker = self.make_sneaker(**kwargs)
            sneakers.append(sneaker)
        return sneakers


class SneakerTestBase(TestCase, SneakerMixin):
    def setUp(self) -> None:
        return super().setUp()
