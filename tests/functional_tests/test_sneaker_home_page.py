import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser


class SneakerBaseFunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)


class SneakerHomePageFunctionalTest(SneakerBaseFunctionalTest):

    def test_sneaker_home_page_without_sneakers_error_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No sneakers found', body.text)
