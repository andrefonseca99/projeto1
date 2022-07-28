import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        ),
            code='Invalid'
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Your first name')
        add_placeholder(self.fields['last_name'], 'Your last name')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    username = forms.CharField(
        error_messages={
            'required': 'This field must not be empty',
            'max_length': 'Username must have less than 150 charcters',
            'min_length': 'Username must have at least 4 charcters',
        },
        label='Username',
        help_text='Can only contain letters, numbers and @/./+/-/_',
        min_length=4,
        max_length=150,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name',
    )

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text=(
            'At leats 8 characters. Needs to contain an uppercase letter, '
            'a lowercase letter and a number'
        ),
        validators=[strong_password],
        label='Password',
        error_messages={'required': 'Password must not be empty'},
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password check',
        error_messages={'required': 'Please repeat your password'},
    )

    class Meta:
        model = User
        fields = [
                'first_name',
                'last_name',
                'username',
                'email',
                'password',
        ]
        # exclude = ['last_name']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Passwords must be equal',
                'password2': 'Passwords must be equal',
            }
            )
