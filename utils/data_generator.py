from faker import Faker

fake = Faker()

class DataGenerator:
    @staticmethod
    def generate_random_email():
        return fake.email()

    @staticmethod
    def generate_random_password():
        return fake.password()

    @staticmethod
    def generate_random_name():
        return fake.name()