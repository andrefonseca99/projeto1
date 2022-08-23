from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import SneakerBaseFunctionalTest


@pytest.mark.functional_test
class SneakerHomePageFunctionalTest(SneakerBaseFunctionalTest):

    @patch('sneakers.views.PER_PAGE', new=2)
    def test_sneaker_home_page_without_sneakers_error_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()
        self.assertIn('No sneakers found', body.text)

    @patch('sneakers.views.PER_PAGE', new=2)
    def test_sneaker_search_input_can_find_correct_sneakers(self):
        sneakers = self.make_sneaker_in_batch()

        title_needed = 'This is what I need'

        sneakers[0].title = title_needed
        sneakers[0].save()

        # Opening the page
        self.browser.get(self.live_server_url)

        # Look for search input with placeholder = "Search for sneakers..."
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a sneaker..."]'
        )

        # Type search term and press ENTER
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('sneakers.views.PER_PAGE', new=2)
    def test_sneaker_home_page_pagination(self):
        self.make_sneaker_in_batch()

        # Opening the page
        self.browser.get(self.live_server_url)

        # Search for pagination and click on page number 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Look for 2 sneakers on second page
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'sneakers')),
            2
        )
