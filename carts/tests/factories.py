from random import randint

import factory

from carts.models import Cart, CartItem
from items.tests.factories import ItemFactory
from users.tests.factories import UserFactory


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def items(self, create, extracted):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.items.add(item)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    quantity = factory.LazyFunction(randint(1, 25))
    item = factory.SubFactory(ItemFactory)
    price = factory.LazyFunction(lambda n: n.item.price)
