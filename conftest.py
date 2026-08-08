import requests
import pytest
import os
from dotenv import load_dotenv
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resources.admin_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles

load_dotenv()

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="function")
def test_user():
    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": [Roles.USER]
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user

@pytest.fixture
def login_data(registered_user):
    return {
        'email': registered_user['email'],
        'password': registered_user['password']
    }

@pytest.fixture(scope="session")
def unauth_api_manager():
    session = requests.Session()
    return ApiManager(session)

@pytest.fixture
def user_api_manager():
    session = requests.Session()
    api_manager = ApiManager(session)
    password = DataGenerator.generate_random_password()
    user_data = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }
    response = api_manager.auth_api.register_user(user_data)
    user_id = response.json()['id']

    api_manager.auth_api.authenticate((user_data['email'], password))
    api_manager.user_id = user_id
    yield api_manager

    api_manager.user_api.delete_user(user_id)

@pytest.fixture
def admin_api_manager():
    session = requests.Session()
    api_manager = ApiManager(session)
    email = os.getenv('SUPER_ADMIN_EMAIL')
    password = os.getenv('SUPER_ADMIN_PASSWORD')
    api_manager.auth_api.authenticate((email, password))
    return api_manager

@pytest.fixture
def multiple_users(api_manager):
    ids = []
    for _ in range(3):
        password = DataGenerator.generate_random_password()
        data = {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "roles": ["USER"]
        }
        response = api_manager.auth_api.register_user(data)
        ids.append(response.json()['id'])
    return ids

@pytest.fixture
def movie_data():
    return {
        "name": DataGenerator.generate_random_name(),
        "imageUrl": "https://image.url",
        "price": DataGenerator.generate_random_price(),
        "description": DataGenerator.generate_random_description(),
        "location": DataGenerator.generate_random_location(),
        "published": DataGenerator.generate_random_published(),
        "genreId": 8
    }

@pytest.fixture
def update_movie_data():
    return {
        "name": DataGenerator.generate_random_name(),
        "price": DataGenerator.generate_random_price()
    }

@pytest.fixture
def create_movie(super_admin, movie_data):
    response = super_admin.api.movies_api.create_movie(movie_data)
    movie = response.json()
    yield movie

    try:
        super_admin.api.movies_api.delete_movie_by_id(movie['id'])
    except ValueError as e:
        if '404' in str(e):
            pass
        else:
            raise

@pytest.fixture
def review_data():
    return {
        "rating": DataGenerator.generate_random_rating(),
        "text": DataGenerator.generate_random_review_text()
    }

@pytest.fixture
def update_review_data():
    return {
        "rating": DataGenerator.generate_random_rating(),
        "text": DataGenerator.generate_random_review_text()
    }

@pytest.fixture
def available_genres(unauth_api_manager):
    response = unauth_api_manager.genres_api.get_genres()
    genres = response.json()
    return [genre['id'] for genre in genres]

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        'verified': True,
        'banned': False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user