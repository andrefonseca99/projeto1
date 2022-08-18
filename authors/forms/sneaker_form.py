from collections import defaultdict

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
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
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
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        sneaker_description = cleaned_data.get('sneaker_description')

        if len(title) < 5:
            self._my_errors['title'].append(
                'Title must have at least 5 characthers'
            )

        if title == description:
            self._my_errors['title'].append(
                'Title needs to be different from description'
            )
            self._my_errors['description'].append(
                'Description needs to be different from title'
            )

        if price < 5:
            self._my_errors['price'].append(
                'Sneaker minimum price is R$5,00'
            )
        if price > 100000:
            self._my_errors['price'].append(
                'Sneaker maximum price is R$100.000,00'
            )

        if len(sneaker_description) < 30:
            self._my_errors['sneaker_description'].append(
                'Sneaker description must have at least 30 charachters'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
