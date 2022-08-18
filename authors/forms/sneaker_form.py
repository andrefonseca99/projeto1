from django import forms
from sneakers.models import Sneaker
from utils.django_forms import add_attr


class AuthorsSneakerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields.get('sneaker_description'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Sneaker
        fields = 'title', 'description', 'condition_value', 'price', \
            'sneaker_description', 'cover'
