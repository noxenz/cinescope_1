import allure
from pytest_check import check
import pytest
from constants.roles import Roles
from utils.assertions import validate_movies_response, validate_movie_response

@allure.epic('Movies API')
@allure.feature('Фильмы')
class TestPositive:

    @allure.story('Получение списка фильмов')
    @allure.title('Получение списка фильмов без авторизации')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_movies_list_unauthorized(self, unauth_api_manager):
        with allure.step('Отправка запроса GET /movies без авторизации'):
            response = unauth_api_manager.movies_api.get_movies_list().json()

        with allure.step('Проверка, что список фильмов возвращается'):
            assert 'movies' in response
            assert isinstance(response['movies'], list)

        with allure.step('Проверка структуры ответа'):
            validate_movies_response(response['movies'])

    @allure.story('Получение списка фильмов')
    @allure.title('Получение списка фильмов обычным пользователем')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_get_movies_list_by_common_user(self, common_user):
        with allure.step('ОТправка запроса GET /movies авторизованным пользователем'):
            response = common_user.api.movies_api.get_movies_list().json()

        with allure.step('Проверка, что список фильмов возвращается'):
            assert 'movies' in response
            assert isinstance(response['movies'], list)

        with allure.step('Проверка структуры ответа'):
            validate_movies_response(response['movies'])

    @allure.story('Получение списка фильмов')
    @allure.title('Параметризированная фильтрация фильмов')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize('filter_params,expected_field,expected_value', [
        ({'minPrice': 100, 'maxPrice': 500}, 'price', lambda p: 100 <= p <= 500),
        ({'locations': 'MSK'}, 'location', 'MSK'),
        ({'genreId': 8}, 'genreId', 8)
    ], ids=['Price between 100 and 500', 'Location MSK', 'GenreId 8'])
    def test_get_movies_parametrized(self, super_admin, filter_params, expected_field, expected_value):
        with allure.step(f'Отправка запроса с фильтром {filter_params}'):
            response = super_admin.api.movies_api.get_movies_list(params=filter_params).json()

        with allure.step(f'Проверка, что все фильмы соответствуют фильтру {expected_field}={expected_value}'):
            assert response['movies'], 'Список фильмов пуст'
            for movie_data in response['movies']:
                if expected_field == 'price':
                    with check:
                        assert expected_value(movie_data[expected_field]), f'Цена {movie_data['price']} вне диапазона'
                else:
                    with check:
                        assert movie_data[expected_field] == expected_value, f'Поле {expected_field} = {movie_data[expected_field]}, ожидалось {expected_value}'

    @allure.story('Создание фильма')
    @allure.title('Создание фильма с проверкой в БД')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_movie(self, super_admin, create_movie, movie_data, db_helper):
        with allure.step('Проверка структуры ответа через Pydantic'):
            validate_movie_response(create_movie)

        with allure.step('Проверка соответствия данных'):
            assert create_movie['name'] == movie_data['name']

        with allure.step('Проверка, что фильм появился в БД'):
            movie_in_db = db_helper.get_movie_by_id(create_movie['id'])
            assert movie_in_db is not None
            assert movie_in_db.name == movie_data['name']

    @allure.story('Получение фильма по ID')
    @allure.title('Получение фильма по ID без авторизации')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_movie_by_id_unauthorized(self, unauth_api_manager, create_movie):
        movie_id = create_movie['id']

        with allure.step(f'Отправка запроса GET /movies/{movie_id}'):
            response = unauth_api_manager.movies_api.get_movie_by_id(movie_id).json()

        with allure.step('Проверка ответа через Pydantic'):
            validate_movie_response(response)

        with allure.step('Проверка соответствия данных'):
            assert response['id'] == movie_id
            assert response['name'] == create_movie['name']

    @allure.story('Удаление фильма')
    @allure.title('Удаление фильма суперадмином')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_delete_movie_by_super_admin(self, super_admin, create_movie, db_helper):
        movie_id = create_movie['id']

        with allure.step(f'Удаление фильма {movie_id} суперадмином'):
            super_admin.api.movies_api.delete_movie_by_id(movie_id)

        with allure.step('Проверка, что фильм удалился из БД'):
            movie_in_db = db_helper.get_movie_by_id(movie_id)
            assert movie_in_db is None, f'Фильм {movie_id} присутствует в БД'

    @allure.story('Обновление фильма')
    @allure.title('Обновление фильма по ID суперадмином')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_update_movie_by_id(self, super_admin, create_movie, update_movie_data, db_helper):
        movie_id = create_movie['id']

        with allure.step(f'Отправка PATCH запроса на обновление фильма {movie_id}'):
            response = super_admin.api.movies_api.update_movie_by_id(movie_id, update_movie_data).json()

        with allure.step('Проверка ответа через Pydantic'):
            validate_movie_response(response)

        with allure.step('Проверка соответствия данных'):
            assert response['id'] == movie_id
            assert response['name'] == update_movie_data['name']
            assert response['price'] == update_movie_data['price']

        with allure.step('Проверка, что данные обновились в БД'):
            movie_in_db = db_helper.get_movie_by_id(movie_id)
            assert movie_in_db is not None
            assert movie_in_db.name == update_movie_data['name']
            assert movie_in_db.price == update_movie_data['price']

@allure.epic('Movies API')
@allure.feature('Фильмы (негативные сценарии)')
class TestNegative:

    @allure.story('Создание фильма')
    @allure.title('Создание фильма обычным пользователем')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_movie_as_user(self, common_user, movie_data):
        with allure.step('Попытка создать фильм без прав'):
            response = common_user.api.movies_api.create_movie(movie_data, expected_status=403)
            assert 'Forbidden' in response.text

    @allure.story('Обновление фильма')
    @allure.title('Обновление фильма обычным пользователем')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_update_movie_by_id_as_user(self, common_user, create_movie, update_movie_data):
        movie_id = create_movie['id']

        with allure.step('Попытка обновить фильм без прав'):
            common_user.api.movies_api.update_movie_by_id(movie_id, update_movie_data, expected_status=403)

    @allure.story('Удаление фильма')
    @allure.title('Удаление фильма по ID разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize('role,expected_status', [
        (Roles.ADMIN.value, 403),
        (Roles.USER.value, 403),
        ('unauth', 401)
    ], ids=['admin_cannot_delete', 'common_user_cannot_delete', 'unauth_cannot_delete'])
    def test_delete_movie_by_id(self, request, create_movie, role, expected_status):
        movie_id = create_movie['id']

        with allure.step(f'Получение API менеджера для роли {role}'):
            if role == 'unauth':
                api_manager = request.getfixturevalue('unauth_api_manager')
            else:
                if role == Roles.ADMIN.value:
                    user = request.getfixturevalue('admin_user')
                elif role == Roles.USER.value:
                    user = request.getfixturevalue('common_user')
                else:
                    raise ValueError(f'Неизвестная роль {role}')

                api_manager = user.api

        with allure.step(f'Попытка удалить фильм {movie_id} пользователем с ролья {role}'):
            api_manager.movies_api.delete_movie_by_id(movie_id, expected_status=expected_status)