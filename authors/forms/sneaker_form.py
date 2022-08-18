from django import forms
from sneakers.models import Sneaker


class AuthorsSneakerForm(forms.ModelForm):
    class Meta:
        model = Sneaker
        fields = 'title', 'description', 'condition_value', 'price', \
            'sneaker_description', 'cover'
