from collections import defaultdict

from django.core.exceptions import ValidationError


class AuthorsSneakerValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        cd = self.data

        title = cd.get('title')
        description = cd.get('description')
        price = cd.get('price')
        sneaker_description = cd.get('sneaker_description')

        if len(title) < 5:
            self.errors['title'].append(
                'Title must have at least 5 characthers'
            )

        if title == description:
            self.errors['title'].append(
                'Title needs to be different from description'
            )
            self.errors['description'].append(
                'Description needs to be different from title'
            )

        if price < 5:
            self.errors['price'].append(
                'Sneaker minimum price is R$5,00'
            )
        if price > 100000:
            self.errors['price'].append(
                'Sneaker maximum price is R$100.000,00'
            )

        if len(sneaker_description) < 30:
            self.errors['sneaker_description'].append(
                'Sneaker description must have at least 30 charachters'
            )

        if self.errors:
            raise self.ErrorClass(self.errors)
