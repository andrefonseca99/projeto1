from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_sneaker_base import Sneaker, SneakerTestBase


class SneakerModelTest(SneakerTestBase):

    def setUp(self) -> None:
        self.sneaker = self.make_sneaker()
        return super().setUp()

    def make_sneaker_no_defaults(self):
        sneaker = Sneaker(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Sneaker Title',
            description='Sneaker Description',
            slug='sneaker-slug',
            condition_value=10,
            condition_unit='/10',
            price=100,
            price_unit='R$',
            sneaker_description='Sneaker condition description',
            cover='media\\sneakers\\covers\2022\06\15\\WhatsApp_Image_2022-06-15_at_11.24.14.jpeg'  # noqa: E501
        )
        sneaker.full_clean()
        sneaker.save()
        return sneaker

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('condition_unit', 65),
            ('price_unit', 65),
        ])
    def test_sneaker_fields_max_length(self, field, max_length):
        setattr(self.sneaker, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.sneaker.full_clean()

    def test_sneaker_description_is_html_is_false_by_default(self):
        sneaker = self.make_sneaker_no_defaults()
        self.assertFalse(sneaker.sneaker_description_is_html)

    def test_sneaker_is_published_is_false_by_default(self):
        sneaker = self.make_sneaker_no_defaults()
        self.assertFalse(sneaker.is_published)

    def test_sneaker_string_representation(self):
        needed = 'Testing Representation'
        self.sneaker.title = needed
        self.sneaker.full_clean()
        self.sneaker.save()
        str(self.sneaker)
        self.assertEqual(str(self.sneaker), needed)
