from data.auth.register_data import get_register_payload, get_wrong_login_payload

# def test_register(auth_api):
#     payload = get_register_payload()
#     response = auth_api.send_request(
#         'POST',
#         '/register',
#         data=payload,
#         expected_status=201
#     )
#     assert response.status_code == 201

# def test_login(auth_api, user_credentials):
#     response = auth_api.send_request(
#         'POST',
#         '/login',
#         data=user_credentials,
#         expected_status=201
#     )
#     assert response.status_code == 201 # В материале написано 200, но по факту возвращает 201
#
#     token = response.json()['accessToken']
#     auth_api.update_session_headers({'Authorization': f'Bearer {token}'})

def test_wrong_login(auth_api):
    payload = get_wrong_login_payload()
    response = auth_api.send_request(
        'POST',
        '/login',
        data=payload,
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

def test_register_user(auth_api, test_user):
    response = auth_api.register_user(test_user)
    assert response.json()['email'] == test_user['email']

def test_login_user(auth_api, login_data):
    response = auth_api.login_user(login_data)
    assert response.status_code == 201

def test_logout_user(auth_api, login_data):
    login_response = auth_api.login_user(login_data)
    assert login_response.status_code == 201

    logout_response = auth_api.logout_user()
    assert logout_response.status_code == 200

class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        # добавим еше проверок
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]


def test_direct_update_headers(api_manager):
    api_manager.auth_api._update_session_headers({'foo': 'bar'})

    headers = api_manager.auth_api.session.headers
    assert headers.get('foo') == 'bar'
    print('Заголовок foo есть в сессии: ', headers)

def test_get_user_info_unauth(unauth_api_manager, registered_user):
    user_id = registered_user['id']
    response = unauth_api_manager.user_api.get_user_info(user_id, expected_status=401)
    assert response.status_code == 401

def test_get_user_info(admin_api_manager, registered_user):
    user_id = registered_user['id']
    response = admin_api_manager.user_api.get_user_info(user_id)
    assert response.status_code == 200
    assert response.json()['email'] == registered_user['email']
    assert response.json()['id'] == registered_user['id']

import pytest
import requests

def test_register_timeout(api_manager, test_user):
    with pytest.raises(requests.exceptions.ConnectTimeout):
        api_manager.auth_api.register_user(test_user, timeout=0.001)


def test_delete_multiple_users(multiple_users, admin_api_manager):
    admin_api_manager.user_api.delete_users(*multiple_users)

    for user_id in multiple_users:
        response = admin_api_manager.user_api.get_user_info(user_id, expected_status=404)
        assert response.status_code == 404