import pytest

class TestPositive:
    @pytest.mark.smoke
    def test_get_movies_list_unauthorized(self, unauth_api_manager):
        response = unauth_api_manager.movies_api.get_movies_list()

        data = response.json()
        assert 'movies' in data
        assert isinstance(data['movies'], list)
        assert len(data['movies']) > 0

        movie = data['movies'][0]
        assert 'id' in movie
        assert 'name' in movie
        assert 'price' in movie

    def test_get_movies_list_by_common_user(self, common_user):
        response = common_user.api.movies_api.get_movies_list().json()
        assert 'movies' in response
        assert isinstance(response['movies'], list)

        movie = response['movies'][0]
        required_fields = ['id', 'name', 'price']
        for field in required_fields:
            assert field in movie, f'Поле {field} отсутствует'

    @pytest.mark.parametrize('filter_params,expected_field,expected_value', [
        ({'minPrice': 100, 'maxPrice': 500}, 'price', lambda p: 100 <= p <= 500),
        ({'locations': 'MSK'}, 'location', 'MSK'),
        ({'genreId': 4}, 'genreId', 4)
    ], ids=['Price between 100 and 500', 'Location MSK', 'GenreId 4'])
    def test_get_movies_parametrized(self, super_admin, filter_params, expected_field, expected_value):
        response = super_admin.api.movies_api.get_movies_list(params=filter_params).json()
        assert 'movies' in response
        for movie in response['movies']:
            if expected_field == 'price':
                assert expected_value(movie[expected_field]), f'Цена {movie['price']} вне дипазона'
            else:
                assert movie[expected_field] == expected_value, f'Поле {expected_field} = {movie[expected_field]}, ожидалось {expected_value}'

    def test_get_movies_list_filter_by_location(self, unauth_api_manager):
        params = {'locations': 'MSK'}
        response = unauth_api_manager.movies_api.get_movies_list(params=params)

        data = response.json()
        assert 'movies' in data
        for movie in data['movies']:
            assert movie['location'] == 'MSK'

    def test_get_movies_list_filter_by_genre(self, unauth_api_manager, available_genres):
        genre_id = available_genres[0]

        params = {'genreId': genre_id}
        response = unauth_api_manager.movies_api.get_movies_list(params=params)

        data = response.json()
        assert 'movies' in data
        for movie in data['movies']:
            assert movie['genreId'] == genre_id

    @pytest.mark.smoke
    def test_create_movie(self, super_admin, create_movie, movie_data):
        assert 'id' in create_movie
        assert create_movie['name'] == movie_data['name']
        assert create_movie['price'] == movie_data['price']

    def test_create_movie_by_user(self, common_user, movie_data):
        common_user.api.movies_api.create_movie(movie_data, expected_status=403)

    @pytest.mark.smoke
    def test_get_movie_by_id_unauthorized(self, unauth_api_manager, create_movie):
        movie_id = create_movie['id']
        response = unauth_api_manager.movies_api.get_movie_by_id(movie_id)

        data = response.json()
        assert data['id'] == movie_id
        assert data['name'] == create_movie['name']

    @pytest.mark.smoke
    @pytest.mark.parametrize()
    def test_delete_movie_by_id(self, super_admin, create_movie):
        movie_id = create_movie['id']
        super_admin.api.movies_api.delete_movie_by_id(movie_id)

        super_admin.api.movies_api.get_movie_by_id(movie_id, expected_status=404)

    @pytest.mark.smoke
    def test_update_movie_by_id(self, super_admin, create_movie, update_movie_data):
        movie_id = create_movie['id']
        response = super_admin.api.movies_api.update_movie_by_id(movie_id, update_movie_data)

        data = response.json()
        assert data['name'] == update_movie_data['name']
        assert data['price'] == update_movie_data['price']
        assert data['id'] == movie_id

    def test_get_movies_reviews_by_id_unauthorized(
            self, unauth_api_manager, super_admin, create_movie, review_data
    ):
        movie_id = create_movie['id']

        super_admin.api.movies_api.post_movie_review_by_id(movie_id, review_data)

        response = unauth_api_manager.movies_api.get_movie_reviews_by_id(movie_id)

        data = response.json()
        review = data[0]
        assert 'userId' in review
        assert 'rating' in review
        assert 'text' in review

    @pytest.mark.xfail(reason='По документации ожидается список, но приходит словарь')
    def test_post_movie_review_by_id(self, common_user, create_movie, review_data):
        movie_id = create_movie['id']
        response = common_user.api.movies_api.post_movie_review_by_id(movie_id, review_data, expected_status=201)

        data = response.json()
        assert isinstance(data, list)

        review = data[0]
        assert review['rating'] == review_data['rating']
        assert review['text'] == review_data['text']
        assert 'userId' in review

    def test_update_movie_review_by_id(self, common_user, create_movie, review_data, update_review_data):
        movie_id = create_movie['id']

        create_response = common_user.api.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        response = common_user.api.movies_api.update_movie_review_by_id(movie_id, update_review_data)

        data = response.json()
        assert data['rating'] == update_review_data['rating']
        assert data['text'] == update_review_data['text']
        assert data['userId'] == user_id

    def test_delete_movie_review_by_id(self, common_user, create_movie, review_data):
        movie_id = create_movie['id']

        common_user.api.movies_api.post_movie_review_by_id(movie_id, review_data)

        response = common_user.api.movies_api.delete_movie_review_by_id(movie_id)

        data = response.json()
        assert 'userId' in data
        assert 'rating' in data
        assert 'text' in data

        get_response = common_user.api.movies_api.get_movie_reviews_by_id(movie_id)
        assert len(get_response.json()) == 0

    def test_hide_movie_review_by_id(self, super_admin, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = super_admin.api.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        super_admin.api.movies_api.hide_movie_review_by_id(movie_id, user_id)

    def test_show_movie_review_by_id(self, super_admin, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = super_admin.api.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        super_admin.api.movies_api.hide_movie_review_by_id(movie_id, user_id)

        super_admin.api.movies_api.show_movie_review_by_id(movie_id, user_id)


class TestNegative:
    @pytest.mark.negative
    def test_create_movie_as_user(self, common_user, movie_data):
        response = common_user.api.movies_api.create_movie(movie_data, expected_status=403)
        assert 'Forbidden' in response.text

    @pytest.mark.negative
    def test_delete_movie_by_id_as_user(self, common_user, create_movie):
        movie_id = create_movie['id']
        response = common_user.api.movies_api.delete_movie_by_id(movie_id, expected_status=403)
        assert 'Forbidden' in response.text

    @pytest.mark.negative
    def test_update_movie_by_id_as_user(self, common_user, create_movie, update_movie_data):
        movie_id = create_movie['id']
        common_user.api.movies_api.update_movie_by_id(movie_id, update_movie_data, expected_status=403)

    @pytest.mark.negative
    def test_post_movie_review_by_id_as_unauthorized(self, unauth_api_manager, create_movie, review_data):
        movie_id = create_movie['id']
        unauth_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data, expected_status=401)

    @pytest.mark.negative
    def test_update_movie_review_by_id_as_user(
            self, super_admin, common_user, create_movie, review_data, update_review_data
    ):
        movie_id = create_movie['id']

        super_admin.api.movies_api.post_movie_review_by_id(movie_id, review_data)

        common_user.api.movies_api.update_movie_review_by_id(movie_id, update_review_data, expected_status=404)

    @pytest.mark.negative
    def test_delete_movie_review_by_id_as_unauthorized(
            self, unauth_api_manager, common_user, create_movie, review_data
    ):
        movie_id = create_movie['id']

        common_user.api.movies_api.post_movie_review_by_id(movie_id, review_data)

        unauth_api_manager.movies_api.delete_movie_review_by_id(movie_id, expected_status=401)

    @pytest.mark.negative
    def test_delete_movie_admin_review_by_id_as_user(
            self, super_admin, common_user, create_movie, review_data
    ):
        movie_id = create_movie['id']

        super_admin.api.movies_api.post_movie_review_by_id(movie_id, review_data)

        common_user.api.movies_api.delete_movie_review_by_id(movie_id, expected_status=404)

    @pytest.mark.negative
    def test_hide_movie_review_by_id_as_user(self, common_user, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = common_user.api.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        common_user.api.movies_api.hide_movie_review_by_id(movie_id, user_id, expected_status=403)

    @pytest.mark.negative
    def test_show_movie_review_by_id_as_user(self, common_user, super_admin, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = super_admin.api.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        super_admin.api.movies_api.hide_movie_review_by_id(movie_id, user_id)

        common_user.api.movies_api.show_movie_review_by_id(movie_id, user_id, expected_status=403)