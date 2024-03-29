import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        # User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User looks for login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User types his username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User sends form
        form.submit()

        # User sees successful message and his user
        self.assertIn(
            f'You are logged in with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
            )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # User opens login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User try to login with empty data
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        # User tries to send form
        form.submit()

        # User sees error message
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        # User opens login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User try to login with invalid data
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_username')
        password.send_keys('invalid_password')

        # User tries to send form
        form.submit()

        # User sees error message
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
