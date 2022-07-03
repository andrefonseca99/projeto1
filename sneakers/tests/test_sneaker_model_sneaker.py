from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_sneaker_base import SneakerTestBase


class SneakerModelTest(SneakerTestBase):

    def setUp(self) -> None:
        self.sneaker = self.make_sneaker()
        return super().setUp()

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
