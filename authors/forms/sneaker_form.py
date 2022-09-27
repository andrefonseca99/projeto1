from collections import defaultdict

from authors.validators import AuthorsSneakerValidator
from django import forms
from django.core.exceptions import ValidationError
from sneakers.models import Sneaker
from utils.django_forms import add_attr


class AuthorsSneakerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('sneaker_description'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Sneaker
        fields = 'title', 'description', 'condition_value', 'price', \
            'sneaker_description', 'cover'
        widgets = {
            'condition_value': forms.Select(
                choices=(
                    ('10', '10/10'),
                    ('9', '9/10'),
                    ('8', '8/10'),
                    ('7', '7/10'),
                    ('6', '6/10'),
                    ('5', '5/10'),
                    ('4', '4/10'),
                    ('3', '3/10'),
                    ('2', '2/10'),
                    ('1', '1/10'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorsSneakerValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
