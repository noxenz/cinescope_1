import requests
from custom_requester.custom_requester import CustomRequester

session = requests.Session()
requester = CustomRequester(session=session, base_url='https://auth.dev-cinescope.coconutqa.ru')

def test_login():
    response = requester.send_request(
        'POST',
        'https://auth.dev-cinescope.coconutqa.ru/login',
        data={'email': 'api1@gmail.com', 'password': 'asdqwe123Q'}
    )
    assert response.status_code == 201 # В материале написано 200, но по факту возвращает 201