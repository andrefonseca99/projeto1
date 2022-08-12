from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


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
        help_text='The e-mail must be valid.',
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
                )

        return email

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
