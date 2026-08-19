import pytest
from constants.roles import Roles
from models.base_models import RegisterUserResponse

class TestPositive:
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponse(**response.json())

        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True

    @pytest.mark.xfail(reason='Нельзя создать админа')
    def test_create_admin(self, super_admin, creation_user_data):
        creation_user_data.roles = [Roles.ADMIN]
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        created_user = RegisterUserResponse(**response)

        assert created_user.email == creation_user_data.email
        assert created_user.roles == creation_user_data.roles

    def test_get_user_by_id(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        created_user = RegisterUserResponse(**response)

        response_by_id = super_admin.api.user_api.get_user_info(created_user.id).json()
        user_by_id = RegisterUserResponse(**response_by_id)

        response_by_email = super_admin.api.user_api.get_user_info(creation_user_data.email).json()
        user_by_email = RegisterUserResponse(**response_by_email)

        assert user_by_id == user_by_email, "Содержание ответов должно быть идентичным"
        assert user_by_id.email == creation_user_data.email
        assert user_by_id.fullName == creation_user_data.fullName
        assert user_by_id.roles == creation_user_data.roles
        assert user_by_id.verified is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    def test_delete_multiple_users(self, multiple_users, admin_api_manager):
        admin_api_manager.user_api.delete_users(*multiple_users)

        for user_id in multiple_users:
            response = admin_api_manager.user_api.get_user_info(user_id)
            assert response.json() == {}

    def test_get_user_info(self, admin_api_manager, registered_user):
        user_id = registered_user.id

        response = admin_api_manager.user_api.get_user_info(user_id).json()
        user_data = RegisterUserResponse(**response)
        assert user_data.email == registered_user.email
        assert user_data.id == registered_user.id

    def test_get_user_info_unauth(self, unauth_api_manager, registered_user):
        user_id = registered_user.id
        unauth_api_manager.user_api.get_user_info(user_id, expected_status=401)