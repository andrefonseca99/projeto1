from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
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
