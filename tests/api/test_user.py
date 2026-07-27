import pytest

class TestPositive:
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', 'ID должен быть не пустым'
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    @pytest.mark.xfail(reason='Нельзя создать админа')
    def test_create_admin(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('email') == creation_user_data['email']
        assert response.get('roles', []) == creation_user_data['roles']

    def test_get_user_by_id(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user_info(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user_info(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    def test_delete_multiple_users(self, multiple_users, admin_api_manager):
        admin_api_manager.user_api.delete_users(*multiple_users)

        for user_id in multiple_users:
            response = admin_api_manager.user_api.get_user_info(user_id)
            assert response.json() == {}

    def test_get_user_info(self, admin_api_manager, registered_user):
        user_id = registered_user['id']

        response = admin_api_manager.user_api.get_user_info(user_id)
        assert response.json()['email'] == registered_user['email']
        assert response.json()['id'] == registered_user['id']

    def test_get_user_info_unauth(self, unauth_api_manager, registered_user):
        user_id = registered_user['id']
        unauth_api_manager.user_api.get_user_info(user_id, expected_status=401)