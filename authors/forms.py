from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Your first name')
        add_placeholder(self.fields['last_name'], 'Your last name')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
        }),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here',
        }),
    )

    class Meta:
        model = User
        fields = [
                'first_name',
                'last_name',
                'username',
                'email',
                'password'
        ]
        # exclude = ['last_name']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'password': None,
            'username': None,
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'max_lenght': 'This field must have less than 3 charcters',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
                # 'class': 'input text_input',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type your last name here',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Type your e-mail here',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password and password2 must be equal',
                'password2': 'Password and password2 must be equal',
            }
            )
