from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories import UserFactory

User = get_user_model()


class CurrentUserViewSetRetrieveTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.url = reverse("user-current")

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
                "id": self.user.id,
                "username": f"{self.user.username}",
                "email": f"{self.user.email}",
                "first_name": f"{self.user.first_name}",
                "last_name": f"{self.user.last_name}",
                "middle_name": f"{self.user.middle_name}",
                "phone": f"{self.user.phone}",
                "address": f"{self.user.address}"
            }
        )


class CurrentUserViewSetUpdateTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.url = reverse("user-current")

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "username": f"test",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "middle_name": "string",
            "phone": "string",
            "address": "string",
            "password": "New_password@!1234"
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.user.id,
                "username": f"{self.user.username}",
                "email": f"{self.user.email}",
                "first_name": f"{self.user.first_name}",
                "last_name": f"{self.user.last_name}",
                "middle_name": f"{self.user.middle_name}",
                "phone": f"{self.user.phone}",
                "address": f"{self.user.address}"
            }
        )


class CurrentUserViewSetPartialUpdateTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-current")

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "middle_name": "string",
            "phone": "string",
            "address": "string"
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.user.id,
                "username": f"{self.user.username}",
                "email": f"{self.user.email}",
                "first_name": f"{self.user.first_name}",
                "last_name": f"{self.user.last_name}",
                "middle_name": f"{self.user.middle_name}",
                "phone": f"{self.user.phone}",
                "address": f"{self.user.address}"
            }
        )


class RegisterAPIViewCreateTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-register")

    def test(self):
        data = {
            "password": "Test1!",
            "email": "test@example.com",
            "first_name": "string",
            "last_name": "string",
            "middle_name": "string",
            "phone": "string",
            "address": "string",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(id=response.json()["id"])
        self.assertEqual(
            response.json(),
            {
                "id": user.id,
                "username": f"{user.username}",
                "email": f"{user.email}",
                "first_name": f"{user.first_name}",
                "last_name": f"{user.last_name}",
                "middle_name": f"{user.middle_name}",
                "phone": f"{user.phone}",
                "address": f"{user.address}"
            }
        )
