import random
from random import randint
import decimal
import factory.fuzzy

from items.models import Item


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    title = factory.sequence(lambda n: f'Item - {n}')
    description = factory.sequence(lambda n: f'Description - {n}')
    image = factory.django.ImageField()
    weight = factory.sequence(lambda n: n)
    price = factory.fuzzy.FuzzyDecimal(800.00, 1700.00)
