import requests
import pytest
import os
from dotenv import load_dotenv
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resources.admin_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from models.base_models import TestUser, RegisterUserResponse
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.helpers import DBHelper
from playwright.sync_api import Page
from utils.tools import Tools

from pages.register_page import CinescopeRegisterPage
from pages.login_page import CinescopeLoginPage
from pages.movie_page import CinescopeMoviePage

DEFAULT_UI_TIMEOUT = 30000

load_dotenv()

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="function")
def test_user() -> TestUser:
    password = DataGenerator.generate_random_password()
    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=password,
        passwordRepeat=password,
        roles=[Roles.USER]
    )

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    return RegisterUserResponse(**response)

@pytest.fixture
def login_data(registered_user, test_user):
    return {
        'email': registered_user.email,
        'password': test_user.password
    }

@pytest.fixture(scope="session")
def unauth_api_manager():
    session = requests.Session()
    return ApiManager(session)

@pytest.fixture
def user_api_manager():
    session = requests.Session()
    api_manager = ApiManager(session)
    password = DataGenerator.generate_random_password()
    user_data = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }
    response = api_manager.auth_api.register_user(user_data)
    user_id = response.json()['id']

    api_manager.auth_api.authenticate((user_data['email'], password))
    api_manager.user_id = user_id
    yield api_manager

    api_manager.user_api.delete_user(user_id)

@pytest.fixture
def admin_api_manager():
    session = requests.Session()
    api_manager = ApiManager(session)
    email = os.getenv('SUPER_ADMIN_EMAIL')
    password = os.getenv('SUPER_ADMIN_PASSWORD')
    api_manager.auth_api.authenticate((email, password))
    return api_manager

@pytest.fixture
def multiple_users(api_manager):
    ids = []
    for _ in range(3):
        password = DataGenerator.generate_random_password()
        data = {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "roles": ["USER"]
        }
        response = api_manager.auth_api.register_user(data)
        ids.append(response.json()['id'])
    return ids

@pytest.fixture
def movie_data():
    return {
        "name": DataGenerator.generate_random_name(),
        "imageUrl": "https://image.url",
        "price": DataGenerator.generate_random_price(),
        "description": DataGenerator.generate_random_description(),
        "location": DataGenerator.generate_random_location(),
        "published": DataGenerator.generate_random_published(),
        "genreId": 8
    }

@pytest.fixture
def update_movie_data():
    return {
        "name": DataGenerator.generate_random_name(),
        "price": DataGenerator.generate_random_price()
    }

@pytest.fixture
def create_movie(super_admin, movie_data):
    response = super_admin.api.movies_api.create_movie(movie_data)
    movie = response.json()
    yield movie

    try:
        super_admin.api.movies_api.delete_movie_by_id(movie['id'])
    except ValueError as e:
        if '404' in str(e):
            pass
        else:
            raise

@pytest.fixture
def review_data():
    return {
        "rating": DataGenerator.generate_random_rating(),
        "text": DataGenerator.generate_random_review_text()
    }

@pytest.fixture
def update_review_data():
    return {
        "rating": DataGenerator.generate_random_rating(),
        "text": DataGenerator.generate_random_review_text()
    }

@pytest.fixture
def available_genres(unauth_api_manager):
    response = unauth_api_manager.genres_api.get_genres()
    genres = response.json()
    return [genre['id'] for genre in genres]

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(update={'verified': True, 'banned': False})

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture(scope='module')
def db_session() -> Session:
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    db_helper.delete_user(user)

@pytest.fixture
def created_test_movie(db_helper):
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    yield movie
    db_helper.delete_movie(movie)

@pytest.fixture(scope='session')
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f'trace_{Tools.get_timestamp()}.zip'
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def register_page(page: Page) -> CinescopeRegisterPage:
    register_page = CinescopeRegisterPage(page)
    register_page.open()
    return register_page

@pytest.fixture
def login_page(page: Page) -> CinescopeLoginPage:
    login_page = CinescopeLoginPage(page)
    return login_page

@pytest.fixture
def logged_in_page(page):
    page.goto("https://dev-cinescope.coconutqa.ru/login")
    page.locator('[data-qa-id="login_email_input"]').fill(os.getenv('SUPER_ADMIN_EMAIL'))
    page.locator('[data-qa-id="login_password_input"]').fill(os.getenv('SUPER_ADMIN_PASSWORD'))
    page.locator('[data-qa-id="login_submit_button"]').click()
    page.wait_for_timeout(2000)
    page.reload()
    page.wait_for_selector('[data-qa-id="profile_page_button"]', timeout=10000)

    return page

@pytest.fixture
def movie_page(page):
    return CinescopeMoviePage(page)