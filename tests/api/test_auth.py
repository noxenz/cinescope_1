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
        }
    )
    assert response.status_code == 201

def test_login(requester, user_credentials):
    response = requester.send_request(
        'POST',
        '/login',
        data=user_credentials
    )
    assert response.status_code == 201 # В материале написано 200, но по факту возвращает 201

def test_get_user(user_id, admin_requester):
    response = admin_requester.send_request(
        'GET',
        f'/user/{user_id}'
    )
    assert response.status_code == 200