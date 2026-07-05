import pytest
import requests
from custom_requester.custom_requester import CustomRequester
from faker import Faker

fake = Faker()

@pytest.fixture
def session():
    return requests.Session()

@pytest.fixture
def requester(session):
    return CustomRequester(
        session=session,
        base_url='https://auth.dev-cinescope.coconutqa.ru'
    )

@pytest.fixture
def user_id(requester):
    # Создаём пользователя
    resp = requester.send_request(
        'POST',
        '/register',
        data={
            "email": fake.email(),
            "fullName": "Test User",
            "password": "12345678Aa",
            "passwordRepeat": "12345678Aa"
        }
    )
    assert resp.status_code == 201
    return resp.json()["id"]

@pytest.fixture
def admin_requester(requester):
    resp = requester.send_request('POST', '/login', data={
        'email': 'api1@gmail.com',
        'password': 'asdqwe123Q'
    })
    token = resp.json()["accessToken"]
    requester.session.headers.update({"Authorization": f"Bearer {token}"})
    return requester


@pytest.fixture
def user_credentials(requester):
    email = fake.email()
    password = "12345678Aa"

    requester.send_request('POST', '/register', data={
        "email": email,
        "fullName": "Test User",
        "password": password,
        "passwordRepeat": password
    })

    return {"email": email, "password": password}