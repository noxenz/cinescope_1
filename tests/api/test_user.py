class TestPositive:
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