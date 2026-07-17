import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator


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
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user

@pytest.fixture(scope="session")
def unauth_api_manager():
    session = requests.Session()
    return ApiManager(session)

@pytest.fixture
def authenticated_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    user_data = response.json()

    api_manager.auth_api.authenticate((test_user['email'], test_user['password']))

    user_data['password'] = test_user['password']
    return user_data


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
    api_manager.auth_api.register_user(user_data)

    # 2. Логинимся под ним
    api_manager.auth_api.authenticate((user_data['email'], password))
    return api_manager

@pytest.fixture
def admin_api_manager(api_manager):
    api_manager.auth_api.authenticate(('api1@gmail.com', 'asdqwe123Q'))
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
def create_movie(admin_api_manager, movie_data):
    response = admin_api_manager.movies_api.create_movie(movie_data)
    movie = response.json()
    yield movie

    try:
        admin_api_manager.movies_api.get_movie_by_id(movie['id'])
        admin_api_manager.movies_api.delete_movie_by_id(movie['id'])
    except Exception:
        pass

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
    response = unauth_api_manager.movies_api.get_movies_list()
    data = response.json()

    genres = list(set(movie['genreId'] for movie in data['movies']))
    return genres