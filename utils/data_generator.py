from faker import Faker
import random
import string
from uuid import uuid4
import datetime

fake = Faker()

class DataGenerator:
    @staticmethod
    def generate_movie_data() -> dict:
        return {
        'name': f'Test Movie {DataGenerator.generate_random_string(5)}',
        'price': DataGenerator.generate_random_int(100, 1000),
        'description': DataGenerator.generate_random_description(),
        'imageUrl': f'https://test.com/{DataGenerator.generate_random_string(8)}.jpg',
        'location': DataGenerator.generate_random_location(),
        'published': True,
        'rating': DataGenerator.generate_random_rating(),
        'genreId': DataGenerator.generate_random_int(7, 10),
        # 'created_at': datetime.datetime.now()
        }

    @staticmethod
    def generate_user_data() -> dict:
        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_random_email():
        return f'{fake.user_name()}{random.randint(1000, 999999)}@example.com'

    @staticmethod
    def generate_random_password():
        return fake.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        ).replace('!', '')

    @staticmethod
    def generate_random_name():
        return fake.first_name() + ' ' + fake.last_name() + ' ' + fake.last_name()

    @staticmethod
    def generate_random_price():
        return random.randint(50, 500)

    @staticmethod
    def generate_random_description():
        return fake.sentence(nb_words=10)

    @staticmethod
    def generate_random_location():
        return random.choice(['MSK', 'SPB'])

    @staticmethod
    def generate_random_published():
        return random.choice([True, False])

    @staticmethod
    def generate_random_review_text():
        return fake.sentence(nb_words=15)

    @staticmethod
    def generate_random_rating():
        return random.randint(1, 5)

    @staticmethod
    def generate_random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def generate_random_int(min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)