from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from items.tests.factories import ItemFactory


class ItemViewSetListTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.items = [ItemFactory() for _ in range(10)]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('items:item-list')

    def test(self):
        response = self.client.get(self.url, format='json')
        results = response.json()['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            results,
            [
                {
                    "id": i.id,
                    "title": i.title,
                    "description": i.description,
                    "image": f'http://testserver{i.image.url}',
                    "weight": i.weight,
                    "price": f'{i.price}',
                } for i in self.items[:len(results)]
            ]
        )


class ItemViewSetRetrieveTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.item = ItemFactory()
        cls.url = reverse('items:item-detail', kwargs={"pk": cls.item.pk})

    def test(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.item.id,
                "title": self.item.title,
                "description": self.item.description,
                "image": f'http://testserver{self.item.image.url}',
                "weight": self.item.weight,
                "price": f'{self.item.price}',
            }
        )
