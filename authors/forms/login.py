from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        add_placeholder(self.fields['username'], 'Type your username')
        add_placeholder(self.fields['password'], 'Type your password')
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
