from faker import Faker
import random

fake = Faker()

class DataGenerator:
    @staticmethod
    def generate_random_email():
        return fake.email()

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
        return fake.first_name() + ' ' + fake.last_name()

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