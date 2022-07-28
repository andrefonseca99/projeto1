from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Can only contain letters, numbers and @/./+/-/_'),
        ('password',
            'At leats 8 characters. Needs to contain an uppercase letter, '
            'a lowercase letter and a number',),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Password check'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label

        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):

    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Stro0ngP@ssword1',
            'password2': 'Stro0ngP@ssword1',
            }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_is_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least 4 charcters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_is_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have less than 150 charcters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_has_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        )

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_field_matches_password2_field(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1234'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Passwords must be equal'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
