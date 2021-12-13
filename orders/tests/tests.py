from random import randint
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from carts.models import Cart, CartItem
from items.tests.factories import ItemFactory
from orders.models import Order
from users.tests.factories import UserFactory


class OrderViewSetListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('orders:order-list')

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
        self.total_cost = 0
        for item in self.cart_items_models:
            self.total_cost += item.price * item.quantity
        self.orders = [
            Order.objects.create(
                cart=self.cart,
                address=f'test address - {_}',
                delivery_at=timezone.now(),
                total_cost=self.total_cost,
                recipient=self.user
            )
            for _ in range(20)
        ]

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
                    "id": order.id,
                    "cart": {
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

                        "total_cost": float(self.total_cost)
                    },
                    "status": f"{order.status}",
                    "total_cost": float(self.total_cost),
                    "address": f"{order.address}",
                    "delivery_at": f"{str(order.delivery_at)[:19]}",
                    "created_at": f"{str(order.created_at)[:19]}"
                }
                for order in self.orders[:len(results)]
            ]
        )


class OrderViewSetCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('orders:order-list')

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
        self.total_cost = 0
        for item in self.cart_items_models:
            self.total_cost += item.price * item.quantity

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        data = {
            "address": "string",
            "delivery_at": "2021-05-22 13:47:10.954Z"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.json()['id'])
        self.assertEqual(
            response.json(),
            {
                "id": order.id,
                "cart": {
                    "id": self.cart.id,
                    "cart_items": [
                        {
                            "id": cart_item.pk,
                            "item": {
                                "id": cart_item.item.id,
                                "title": f"{cart_item.item.title}",
                                "description": f"{cart_item.item.description}",
                                "image": f"http://testserver{cart_item.item.image.url}",
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

                    "total_cost": float(self.total_cost)
                },
                "status": f"{order.status}",
                "total_cost": float(self.total_cost),
                "address": f"{order.address}",
                "delivery_at": f"{str(order.delivery_at)[:23]}Z",
                "created_at": f"{str(order.created_at)[:19]}"
            }
        )


class OrderViewSetPartialUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        cls.cart_items_id = []
        cls.cart_items_models = []
        for _ in range(20):
            item = ItemFactory()
            cart_item = CartItem.objects.create(cart=cls.cart, item=item, quantity=randint(1, 100), price=item.price)
            cls.cart_items_id.append(cart_item.id)
            cls.cart_items_models.append(cart_item)
        cls.cart.items.set(cls.cart_items_id)
        cls.total_cost = 0
        for item in cls.cart_items_models:
            cls.total_cost += item.price * item.quantity
        cls.ok_order = Order.objects.create(
            cart=cls.cart,
            address='test address',
            delivery_at=timezone.now(),
            total_cost=cls.total_cost,
            recipient_id=cls.user.id,
        )
        cls.url = reverse('orders:order-detail', kwargs={"pk": cls.ok_order.id})

    def setUp(self) -> None:
        self.fail_order = Order.objects.create(
            cart=self.cart,
            address='test address',
            delivery_at=timezone.now(),
            total_cost=self.total_cost,
            recipient=self.user,
            recipient_id=self.user.id,
            status='delivered',
        )

    def test_unauthorized(self):
        data = {
            "status": "created",
            "address": "string",
            "delivery_at": "2021-05-22T13:47:10.954Z"
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test_order_status(self):
        self.client.force_authenticate(user=self.user)
        fail_url = reverse('orders:order-detail', kwargs={"pk": self.fail_order.id})
        data = {
            "status": "created",
            "address": "string",
            "delivery_at": "2021-05-22T13:47:10.954Z"
        }
        response = self.client.put(fail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = 'Вы не можете редактировать заказ в обработке/доставленный заказ/отмененный заказ'
        self.assertEqual(response.json()['data'], message)

    def test(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "status": "created",
            "address": "string",
            "delivery_dt": "2021-05-22T13:47:10.954Z"
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = Order.objects.get(id=response.json()['id'])
        self.assertEqual(
            response.json(),
            {
                "id": order.id,
                "cart": {
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

                    "total_cost": float(self.total_cost)
                },
                "status": f"{order.status}",
                "total_cost": float(self.total_cost),
                "address": f"{order.address}",
                "delivery_at": f"{str(order.delivery_at)[:19]}",
                "created_at": f"{str(order.created_at)[:19]}"
            }
        )


class OrderViewSetUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        cls.cart_items_id = []
        cls.cart_items_models = []
        for _ in range(20):
            item = ItemFactory()
            cart_item = CartItem.objects.create(cart=cls.cart, item=item, quantity=randint(1, 100), price=item.price)
            cls.cart_items_id.append(cart_item.id)
            cls.cart_items_models.append(cart_item)
        cls.cart.items.set(cls.cart_items_id)
        cls.total_cost = 0
        for item in cls.cart_items_models:
            cls.total_cost += item.price * item.quantity
        cls.ok_order = Order.objects.create(
            cart=cls.cart,
            address='test address',
            delivery_at=timezone.now(),
            total_cost=cls.total_cost,
            recipient_id=cls.user.id,
        )
        cls.url = reverse('orders:order-detail', kwargs={"pk": cls.ok_order.id})

    def setUp(self) -> None:
        self.fail_order = Order.objects.create(
            cart=self.cart,
            address='test address',
            delivery_at=timezone.now(),
            total_cost=self.total_cost,
            recipient=self.user,
            recipient_id=self.user.id,
            status='delivered',
        )

    def test_unauthorized(self):
        data = {
            "status": "created",
            "address": "string",
            "delivery_at": "2021-05-22T13:47:10.954Z"
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test_order_status(self):
        self.client.force_authenticate(user=self.user)
        fail_url = reverse('orders:order-detail', kwargs={"pk": self.fail_order.id})
        data = {
            "status": "created",
            "address": "string",
            "delivery_dt": "2021-05-22T13:47:10.954Z"
        }
        response = self.client.put(fail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = 'Вы не можете редактировать заказ в обработке/доставленный заказ/отмененный заказ'
        self.assertEqual(response.json()['data'], message)

    def test(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "status": "created",
            "address": "string",
            "delivery_at": "2021-05-22T13:47:10.954Z"
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = Order.objects.get(id=response.json()['id'])
        self.assertEqual(
            response.json(),
            {
                "id": order.id,
                "cart": {
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

                    "total_cost": float(self.total_cost)
                },
                "status": f"{order.status}",
                "total_cost": float(self.total_cost),
                "address": f"{order.address}",
                "delivery_at": f"{str(order.delivery_at)[:19]}",
                "created_at": f"{str(order.created_at)[:19]}"
            }
        )


class OrderViewSetRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.cart = Cart.objects.create(user=cls.user)
        cls.cart_items_id = []
        cls.cart_items_models = []
        for _ in range(20):
            item = ItemFactory()
            cart_item = CartItem.objects.create(cart=cls.cart, item=item, quantity=randint(1, 100), price=item.price)
            cls.cart_items_id.append(cart_item.id)
            cls.cart_items_models.append(cart_item)
        cls.cart.items.set(cls.cart_items_id)
        cls.total_cost = 0
        for item in cls.cart_items_models:
            cls.total_cost += item.price * item.quantity
        cls.order = Order.objects.create(
            cart=cls.cart,
            address='test address',
            delivery_at=timezone.now(),
            total_cost=cls.total_cost,
            recipient_id=cls.user.id,
        )
        cls.url = reverse('orders:order-detail', kwargs={"pk": cls.order.id})

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
                "id": self.order.id,
                "cart": {
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

                    "total_cost": float(self.total_cost)
                },
                "status": f"{self.order.status}",
                "total_cost": float(self.total_cost),
                "address": f"{self.order.address}",
                "delivery_at": f"{str(self.order.delivery_at)[:19]}",
                "created_at": f"{str(self.order.created_at)[:19]}"
            }
        )
