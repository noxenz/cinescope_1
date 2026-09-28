import allure
import pytest
from utils.data_generator import DataGenerator

@allure.epic('Movies DB')
@allure.feature('Фильмы (БД)')
class TestMoviesDB:

    @allure.story('Создание фильма в БД')
    @allure.title('Проверка создания фильма в БД')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.db
    def test_create_movie_in_db(self, db_helper, created_test_movie):
        with allure.step('Проверка, что фильм есть в БД'):
            movie_in_db = db_helper.get_movie_by_id(created_test_movie.id)
            assert movie_in_db is not None, f'Фильм {created_test_movie.id} не найден в БД'
            assert movie_in_db.name == created_test_movie.name

    @allure.story('Удаление фильма из БД')
    @allure.title('Проверка удаления фильма из БД')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.db
    def test_delete_movie_from_db(self, db_helper):
        with allure.step('Создание фильма в БД'):
            movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
        with allure.step('Удаление фильма'):
            db_helper.delete_movie(movie)
        with allure.step('Проверка, что фильм удален'):
            assert db_helper.get_movie_by_id(movie.id) is None, f'Фильм {movie.id} присутствует в БД'

    @allure.story('Обновление фильма в БД')
    @allure.title('Проверка обновления фильма в БД')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.db
    def test_update_movie_in_db(self, db_helper, created_test_movie):
        with allure.step('Обновление фильма'):
            db_helper.update_movie(created_test_movie, name='Updated Movie', price=150)
        with allure.step('Проверка обновленных данных'):
            movie_in_db = db_helper.get_movie_by_id(created_test_movie.id)
            assert movie_in_db is not None
            assert movie_in_db.name == 'Updated Movie'
            assert movie_in_db.price == 150