from django.core.exceptions import ValidationError

from .test_sneaker_base import SneakerTestBase


class SneakerCategoryModelTest(SneakerTestBase):

    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_sneaker_category_model_string_representation_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_sneaker_category_model_name_max_length(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
