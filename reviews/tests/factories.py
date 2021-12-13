import factory

from reviews.models import Reviews
from users.tests.factories import UserFactory


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reviews

    text = factory.sequence(lambda n: f'Test text - {n}')
    author = factory.SubFactory(UserFactory)
