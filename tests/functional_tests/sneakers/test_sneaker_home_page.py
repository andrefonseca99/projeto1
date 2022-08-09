import pytest
from selenium.webdriver.common.by import By

from .base import SneakerBaseFunctionalTest


@pytest.mark.functional_test
class SneakerHomePageFunctionalTest(SneakerBaseFunctionalTest):

    def test_sneaker_home_page_without_sneakers_error_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No sneakers found', body.text)
