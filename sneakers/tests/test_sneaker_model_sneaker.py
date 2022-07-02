from django.core.exceptions import ValidationError

from .test_sneaker_base import SneakerTestBase


class SneakerModelTest(SneakerTestBase):

    def setUp(self) -> None:
        self.sneaker = self.make_sneaker()
        return super().setUp()

    def test_sneaker_title_raises_error_if_title_is_longer_than_65_chars(self):
        self.sneaker.title = 'A' * 70
        with self.assertRaises(ValidationError):
            self.sneaker.full_clean()
