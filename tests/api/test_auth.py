import pytest
import requests
from models.base_models import TestUser

class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user.email
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_login_user(self, api_manager, login_data):
        response = api_manager.auth_api.login_user(login_data)

        data = response.json()
        assert "accessToken" in data
        assert data["user"]["email"] == login_data["email"]

    def test_logout_user(self, user_api_manager):
        user_id = user_api_manager.user_id
        user_api_manager.auth_api.logout_user()

        user_api_manager.user_api.get_user_info(user_id, expected_status=403)

    def test_refresh_token(self, user_api_manager):
        response = user_api_manager.auth_api.refresh_token()

        data = response.json()
        assert 'accessToken' in data

    def test_register_timeout(self, api_manager, test_user):
        with pytest.raises(requests.exceptions.Timeout):
            api_manager.auth_api.register_user(test_user, timeout=0.001)