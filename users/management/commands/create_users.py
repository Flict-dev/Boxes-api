from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
import requests

user = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        response_user = requests.get(
            'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/recipients.json'
        )
        if response_user.status_code == 200:
            user_json_data = response_user.json()
            for user_json in user_json_data:
                password = user_json['password']
                username = user_json['email']
                user.objects.create_user(
                    username=username.split('@')[0],
                    password=password,
                    first_name=user_json['info']['name'],
                    last_name=user_json['info']['surname'],
                    middle_name=user_json['info']['patronymic'],
                    email=user_json['email'],
                    phone=user_json['contacts']['phoneNumber'],
                    premium=user_json['premium'],
                    address=user_json['city_kladr']
                )
                print(f'success - {username}')
        else:
            print('URL (users) не поддерживается!')
