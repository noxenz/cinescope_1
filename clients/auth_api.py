from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL

REGISTER = '/register'
LOGIN = '/login'
LOGOUT = '/logout'
REFRESH_TOKEN = '/refresh-tokens'
CONFIRM = '/confirm'

class AuthApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def register_user(self, user_data, expected_status=201, **kwargs):
        return self.send_request(
            method='POST',
            endpoint=REGISTER,
            data=user_data,
            expected_status=expected_status,
            **kwargs
        )

    def login_user(self, login_data, expected_status=201, **kwargs):
        return self.send_request(
            method='POST',
            endpoint=LOGIN,
            data=login_data,
            expected_status=expected_status,
            **kwargs
        )

    def logout_user(self, expected_status=200, **kwargs):
        return self.send_request(
            method='GET',
            endpoint=LOGOUT,
            expected_status=expected_status,
            **kwargs
        )

    def refresh_token(self, expected_status=201, **kwargs):
        response = self.send_request(
            method='GET',
            endpoint=REFRESH_TOKEN,
            expected_status=expected_status,
            **kwargs
        )
        token = response.json()['accessToken']
        self._update_session_headers({'authorization': 'Bearer ' + token})
        return response

    def confirm_email(self, token, expected_status=200, **kwargs):
        return self.send_request(
            method='GET',
            endpoint=f'{CONFIRM}/{token}',
            expected_status=expected_status,
            **kwargs
        )

    def authenticate(self, user_creds):
        login_data = {
            'email': user_creds[0],
            'password': user_creds[1]
        }
        response = self.login_user(login_data, expected_status=201).json()
        if 'accessToken' not in response:
            raise KeyError('token is missing')
        token = response['accessToken']
        self._update_session_headers({'authorization': 'Bearer ' + token})