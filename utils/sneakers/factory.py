# from inspect import signature
from random import randint

from faker import Faker


def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
# print(signature(fake.random_number))


def make_sneaker():
    return {
        'title': fake.sentence(nb_words=6),
        'description': fake.sentence(nb_words=12),
        'condition_value': fake.random_number(digits=1, fix_len=True),
        'condition_unit': '/10',
        'price': str(fake.random_number(digits=3, fix_len=True))+',00',
        'price_unit': 'R$',
        'sneaker_description': fake.text(3000),
        'created_at': fake.date_time(),
        'author': {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        },
        'category': {
            'name': fake.word()
        },
        'cover': {
            'url': 'https://loremflickr.com/%s/%s/food,cook' % rand_ratio(),
        },
    }


if __name__ == '__main__':
    from pprint import pprint
    pprint(make_sneaker())
