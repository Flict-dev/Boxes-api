from random import randint
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from carts.models import Cart, CartItem
from items.tests.factories import ItemFactory
from users.tests.factories import UserFactory


class CartViewSetRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('carts:cart-detail')

    def setUp(self) -> None:
        self.user = UserFactory()
        self.cart = Cart.objects.create(user=self.user)
        self.cart_items_id = []
        self.cart_items_models = []
        for _ in range(20):
            item = ItemFactory()
            cart_item = CartItem.objects.create(cart=self.cart, item=item, quantity=randint(1, 100), price=item.price)
            self.cart_items_id.append(cart_item.id)
            self.cart_items_models.append(cart_item)
        self.cart.items.set(self.cart_items_id)

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        total_cost = 0
        for item in self.cart_items_models:
            total_cost += item.price * item.quantity
        self.assertEqual(
            response.json(),
            {
                "id": self.cart.id,
                "cart_items": [
                    {
                        "id": cart_item.pk,
                        "item": {
                            "id": cart_item.item.id,
                            "title": f"{cart_item.item.title}",
                            "description": f"{cart_item.item.description}",
                            "image": f"{cart_item.item.image.url}",
                            "weight": cart_item.item.weight,
                            "price": f"{cart_item.item.price}"
                        },
                        "item_id": cart_item.item.id,
                        "quantity": cart_item.quantity,
                        "price": f'{cart_item.price}',
                        "total_price": float(cart_item.price * cart_item.quantity),
                    }
                    for cart_item in self.cart_items_models
                ],
                "total_cost": float(total_cost)
            }
        )


class CartItemViewSetListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        cls.cart_items = []
        for _ in range(20):
            item = ItemFactory()
            cls.cart_items.append(
                CartItem.objects.create(cart=cls.cart, item=item, quantity=randint(1, 100), price=item.price)
            )
        cls.url = reverse('carts:cart_items-list')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(
            results,
            [
                {
                    "id": cart_item.id,
                    "item": {
                        "id": cart_item.item.id,
                        "title": f"{cart_item.item.title}",
                        "description": f"{cart_item.item.description}",
                        "image": f"{cart_item.item.image.url}",
                        "weight": cart_item.item.weight,
                        "price": f"{cart_item.item.price}"
                    },
                    "item_id": cart_item.id,
                    "quantity": cart_item.quantity,
                    "price": f"{cart_item.price}",
                    "total_price": float(cart_item.quantity * cart_item.price)
                }
                for cart_item in self.cart_items[:len(results)]
            ]
        )


class CartItemViewSetRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        item = ItemFactory()
        cls.cart_item = CartItem.objects.create(cart=cls.cart, item=item, price=item.price, quantity=randint(1, 100))
        cls.url = reverse('carts:cart_items-detail', kwargs={'pk': cls.cart_item.id})

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.cart_item.id,
                "item": {
                    "id": self.cart_item.item.id,
                    "title": f"{self.cart_item.item.title}",
                    "description": f"{self.cart_item.item.description}",
                    "image": f"{self.cart_item.item.image.url}",
                    "weight": self.cart_item.item.weight,
                    "price": f"{self.cart_item.item.price}"
                },
                "item_id": self.cart_item.id,
                "quantity": self.cart_item.quantity,
                "price": f"{self.cart_item.price}",
                "total_price": float(self.cart_item.quantity * self.cart_item.price)
            }
        )


class CartItemViewSetCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('carts:cart_items-list')

    def setUp(self) -> None:
        self.user = UserFactory()
        self.item = ItemFactory()

    def test_unauthorized(self):
        data = {
            "item": self.item.id,
            "quantity": randint(1, 50)
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "item": self.item.id,
            "quantity": randint(1, 50)
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.get(id=response.json()['id'])
        self.assertEqual(
            response.json(),
            {
                "id": cart_item.id,
                "item": {
                    "id": cart_item.item.id,
                    "title": f"{cart_item.item.title}",
                    "description": f"{cart_item.item.description}",
                    "image": f"http://testserver{cart_item.item.image.url}",
                    "weight": cart_item.item.weight,
                    "price": f"{cart_item.item.price}"
                },
                "item_id": cart_item.id,
                "quantity": cart_item.quantity,
                "price": f"{cart_item.price}",
                "total_price": float(cart_item.quantity * cart_item.price)
            }
        )


class CartItemViewSetUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        cls.item = ItemFactory()
        cls.cart_item = CartItem.objects.create(
            item=cls.item, price=cls.item.price, cart=cls.cart, quantity=randint(1, 50)
        )
        cls.new_item = ItemFactory()
        cls.url = reverse('carts:cart_items-detail', kwargs={"pk": cls.cart_item.id})

    def test_unauthorized(self):
        data = {
            "item": self.new_item.id,
            "quantity": randint(1, 50)
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "item": self.new_item.id,
            "quantity": randint(1, 50)
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item = CartItem.objects.get(id=response.json()['id'])
        self.assertEqual(
            response.json(),
            {
                "id": cart_item.id,
                "item": {
                    "id": cart_item.item.id,
                    "title": f"{cart_item.item.title}",
                    "description": f"{cart_item.item.description}",
                    "image": f"http://testserver{cart_item.item.image.url}",
                    "weight": cart_item.item.weight,
                    "price": f"{cart_item.item.price}"
                },
                "item_id": cart_item.id,
                "quantity": cart_item.quantity,
                "price": f"{cart_item.price}",
                "total_price": float(cart_item.quantity * cart_item.price)
            }
        )


class CartItemViewSetPartialUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        cls.item = ItemFactory()
        cls.cart_item = CartItem.objects.create(item=cls.item, price=cls.item.price, cart=cls.cart,
                                                quantity=randint(1, 50))
        cls.url = reverse('carts:cart_items-detail', kwargs={"pk": cls.cart_item.id})

    def test_unauthorized(self):
        data = {
            "item": self.item.id,
            "quantity": randint(1, 50)
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "item": self.item.id,
            "quantity": randint(1, 50)
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item = CartItem.objects.get(id=response.json()['id'])
        self.assertEqual(
            response.json(),
            {
                "id": cart_item.id,
                "item": {
                    "id": cart_item.item.id,
                    "title": f"{cart_item.item.title}",
                    "description": f"{cart_item.item.description}",
                    "image": f"http://testserver{cart_item.item.image.url}",
                    "weight": cart_item.item.weight,
                    "price": f"{cart_item.item.price}"
                },
                "item_id": cart_item.id,
                "quantity": cart_item.quantity,
                "price": f"{cart_item.price}",
                "total_price": float(cart_item.quantity * cart_item.price)
            }
        )


class CartItemViewSetDeleteTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        item = ItemFactory()
        cls.cart_item = CartItem.objects.create(item=item, price=item.price, cart=cls.cart,
                                                quantity=randint(1, 50))
        cls.url = reverse('carts:cart_items-detail', kwargs={"pk": cls.cart_item.id})

    def test_unauthorized(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        try:
            CartItem.objects.get(id=self.cart_item.id)
            self.assertEqual("Test Failed", "Cart doesn't deleted")
        except CartItem.DoesNotExist:
            self.assertEqual("OK", "OK")
