from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from reviews.models import Reviews
from reviews.tests.factories import ReviewFactory
from users.tests.factories import UserFactory


class ReviewViewSetCreateTestCse(APITestCase):
    def setUp(self) -> None:
        self.author = UserFactory()

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('review:reviews-list')

    def test_unauthorized(self):
        response = self.client.post(self.url, data={"text": "test text"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url, data={"text": "test text"})
        review = Reviews.objects.get(id=response.json()['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": review.id,
                "author": {
                    "id": self.author.id,
                    "username": f"{self.author.username}",
                    "email": f"{self.author.email}",
                    "first_name": f"{self.author.first_name}",
                    "last_name": f"{self.author.last_name}",
                    "middle_name": f"{self.author.middle_name}",
                    "phone": f"{self.author.phone}",
                    "address": f"{self.author.address}"
                },
                "status": f"{review.status}",
                "text": f"{review.text}",
                "created_at": f"{review.created_at}",
                "published_at": review.published_at
            }
        )


class ReviewViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.reviews = [ReviewFactory() for _ in range(10)]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('review:reviews-list')

    def test(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(
            results,
            [
                {
                    "id": review.id,
                    "author":
                        {
                            "id": review.author.id,
                            "username": f"{review.author.username}",
                            "email": f"{review.author.email}",
                            "first_name": f"{review.author.first_name}",
                            "last_name": f"{review.author.last_name}",
                            "middle_name": f"{review.author.middle_name}",
                            "phone": f"{review.author.phone}",
                            "address": f"{review.author.address}"
                        },
                    "status": f"{review.status}",
                    "text": f"{review.text}",
                    "created_at": f"{review.created_at}",
                    "published_at": review.published_at
                }
                for review in self.reviews[:len(results)]
            ]
        )
