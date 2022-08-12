import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/div/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)

        return form

    def test_empty_first_name_field_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Your first name')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_field_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Your last name')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_field_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_password_field_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(form, 'Your password')
            password_field.send_keys(' ')
            password_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Password must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_password_check_field_error_message(self):
        def callback(form):
            password_check_field = self.get_by_placeholder(form, 'Repeat your password')  # noqa: E501
            password_check_field.send_keys(' ')
            password_check_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Please repeat your password', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('The e-mail must be valid.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(form, 'Your password')
            password_field.send_keys('P@ssw0rd')

            password_check_field = self.get_by_placeholder(form, 'Repeat your password')  # noqa: E501
            password_check_field.send_keys('P@ssw0rd2')
            password_check_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Passwords must be equal', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Your first name').send_keys('Test')
        self.get_by_placeholder(form, 'Your last name').send_keys('Testing')
        self.get_by_placeholder(form, 'Your username').send_keys('testing')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('email@email.com')  # noqa: E501
        self.get_by_placeholder(form, 'Your password').send_keys('P@ssw0rd')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('P@ssw0rd')  # noqa: E501

        form.submit()

        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
