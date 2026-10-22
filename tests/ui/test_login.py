import allure
import pytest
import os
from playwright.sync_api import expect

@allure.epic('Тестирование UI')
@allure.feature('Вход')
@pytest.mark.ui
@pytest.mark.xfail
class TestLogin:

    @allure.title('Вход в существующий аккаунт')
    def test_login(self, register_page, login_page, page):
        email = os.getenv('SUPER_ADMIN_EMAIL', '')
        password = os.getenv('SUPER_ADMIN_PASSWORD', '')

        login_page.open()
        login_page.login(email, password)

        expect(page).to_have_url(f'{login_page.home_url}')