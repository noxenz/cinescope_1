import requests
from custom_requester.custom_requester import CustomRequester
from faker import Faker

fake = Faker()

# session = requests.Session()
# requester = CustomRequester(session=session, base_url='https://auth.dev-cinescope.coconutqa.ru')

def test_register(requester):
    email = fake.email()
    response = requester.send_request(
        'POST',
        '/register',
        data={
            "email": email,
            "fullName": "Pupu Popo",
            "password": "12345678Aa",
            "passwordRepeat": "12345678Aa"
        },
        expected_status=201
    )
    assert response.status_code == 201

def test_login(requester, user_credentials):
    response = requester.send_request(
        'POST',
        '/login',
        data=user_credentials,
        expected_status=201
    )
    assert response.status_code == 201 # В материале написано 200, но по факту возвращает 201

    token = response.json()['accessToken']
    requester.update_session_headers({'Authorization': f'Bearer {token}'})

def test_wrong_login(requester):
    response = requester.send_request(
        'POST',
        '/login',
        data={
            "email": fake.email(),
            "password": fake.password()
        },
        expected_status=401
    )
    assert response.status_code == 401

def test_get_user(user_id, admin_requester):
    response = admin_requester.send_request(
        'GET',
        f'/user/{user_id}'
    )
    assert response.status_code == 200

def test_get_movies(requester_movie):
    response = requester_movie.send_request(
        'GET',
        '/movies',
        params={'genre': 1, 'pageSize': 10}
    )
    assert response.status_code == 200