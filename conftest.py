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