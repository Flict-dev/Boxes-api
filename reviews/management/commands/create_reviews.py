from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from items.models import Item
from reviews.models import Reviews
from users.models import User
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        response_review = requests.get(
            'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/reviews.json'
        )
        if response_review.status_code == 200:
            json_data_review = response_review.json()
            for review in json_data_review:
                try:
                    Reviews.objects.update_or_create(
                        text=review['content'],
                        author_id=review['author'],
                        created_at=review['created_at'],
                        published_at=review['published_at'],
                        status=review['status']
                    )
                    print('success')
                except ValidationError:
                    Reviews.objects.update_or_create(
                        text=review['content'],
                        author_id=review['author'],
                        created_at=review['created_at'],
                        published_at='2021-01-03',
                        status=review['status']
                    )
        else:
            print('URL (reviews) не поддерживается!')
