import pytest

class TestPositive:
    @pytest.mark.smoke
    def test_get_movies_list_unauthorized(self, unauth_api_manager):
        response = unauth_api_manager.movies_api.get_movies_list()
        assert response.status_code == 200

        data = response.json()
        assert 'movies' in data
        assert isinstance(data['movies'], list)
        assert len(data['movies']) > 0

        if data['movies']:
            movie = data['movies'][0]
            assert 'id' in movie
            assert 'name' in movie
            assert 'price' in movie

    def test_get_movies_list_filter_by_location(self, unauth_api_manager):
        params = {'locations': 'MSK'}
        response = unauth_api_manager.movies_api.get_movies_list(params=params)
        assert response.status_code == 200

        data = response.json()
        assert 'movies' in data
        for movie in data['movies']:
            assert movie['location'] == 'MSK'

    def test_get_movies_list_filter_by_genre(self, unauth_api_manager, available_genres):
        genre_id = available_genres[0]

        params = {'genreId': genre_id}
        response = unauth_api_manager.movies_api.get_movies_list(params=params)
        assert response.status_code == 200

        data = response.json()
        assert 'movies' in data
        for movie in data['movies']:
            assert movie['genreId'] == genre_id

    @pytest.mark.smoke
    def test_create_movie(self, admin_api_manager, movie_data):
        response = admin_api_manager.movies_api.create_movie(movie_data)
        assert response.status_code == 201

        data = response.json()
        assert 'id' in data
        assert data['name'] == movie_data['name']
        assert data['price'] == movie_data['price']

    @pytest.mark.smoke
    def test_get_movie_by_id_unauthorized(self, unauth_api_manager, create_movie):
        movie_id = create_movie['id']
        response = unauth_api_manager.movies_api.get_movie_by_id(movie_id)
        assert response.status_code == 200

        data = response.json()
        assert data['id'] == movie_id
        assert data['name'] == create_movie['name']

    @pytest.mark.smoke
    def test_delete_movie_by_id(self, admin_api_manager, create_movie):
        movie_id = create_movie['id']
        response = admin_api_manager.movies_api.delete_movie_by_id(movie_id)
        assert response.status_code == 200

        get_response = admin_api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert get_response.status_code == 404

    @pytest.mark.smoke
    def test_update_movie_by_id(self, admin_api_manager, create_movie, update_movie_data):
        movie_id = create_movie['id']
        response = admin_api_manager.movies_api.update_movie_by_id(movie_id, update_movie_data)
        assert response.status_code == 200

        data = response.json()
        assert data['name'] == update_movie_data['name']
        assert data['price'] == update_movie_data['price']
        assert data['id'] == movie_id

    def test_get_movies_reviews_by_id_unauthorized(
            self, unauth_api_manager, admin_api_manager, create_movie, review_data
    ):
        movie_id = create_movie['id']

        admin_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)

        response = unauth_api_manager.movies_api.get_movie_reviews_by_id(movie_id)
        assert response.status_code == 200

        data = response.json()
        review = data[0]
        assert 'userId' in review
        assert 'rating' in review
        assert 'text' in review

    @pytest.mark.xfail(reason='По документации ожидается список, но приходит словарь')
    def test_post_movie_review_by_id(self, user_api_manager, create_movie, review_data):
        movie_id = create_movie['id']
        response = user_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)
        assert response.status_code == 201

        data = response.json()
        assert isinstance(data, list)

        review = data[0]
        assert review['rating'] == review_data['rating']
        assert review['text'] == review_data['text']
        assert 'userId' in review

    def test_update_movie_review_by_id(self, user_api_manager, create_movie, review_data, update_review_data):
        movie_id = create_movie['id']

        create_response = user_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        response = user_api_manager.movies_api.update_movie_review_by_id(movie_id, update_review_data)
        assert response.status_code == 200

        data = response.json()
        assert data['rating'] == update_review_data['rating']
        assert data['text'] == update_review_data['text']
        assert data['userId'] == user_id

    def test_delete_movie_review_by_id(self, user_api_manager, create_movie, review_data):
        movie_id = create_movie['id']

        user_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)

        response = user_api_manager.movies_api.delete_movie_review_by_id(movie_id)
        assert response.status_code == 200

        data = response.json()
        assert 'userId' in data
        assert 'rating' in data
        assert 'text' in data

        get_response = user_api_manager.movies_api.get_movie_reviews_by_id(movie_id)
        assert len(get_response.json()) == 0

    def test_hide_movie_review_by_id(self, admin_api_manager, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = admin_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        response = admin_api_manager.movies_api.hide_movie_review_by_id(movie_id, user_id)
        assert response.status_code == 200

    def test_show_movie_review_by_id(self, admin_api_manager, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = admin_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        admin_api_manager.movies_api.hide_movie_review_by_id(movie_id, user_id)

        response = admin_api_manager.movies_api.show_movie_review_by_id(movie_id, user_id)
        assert response.status_code == 200


class TestNegative:
    @pytest.mark.negative
    def test_create_movie_as_user(self, user_api_manager, movie_data):
        response = user_api_manager.movies_api.create_movie(movie_data, expected_status=403)
        assert response.status_code == 403
        assert 'Forbidden' in response.text

    @pytest.mark.negative
    def test_delete_movie_by_id_as_user(self, user_api_manager, create_movie):
        movie_id = create_movie['id']
        response = user_api_manager.movies_api.delete_movie_by_id(movie_id, expected_status=403)
        assert response.status_code == 403
        assert 'Forbidden' in response.text

    @pytest.mark.negative
    def test_update_movie_by_id_as_user(self, user_api_manager, create_movie, update_movie_data):
        movie_id = create_movie['id']
        response = user_api_manager.movies_api.update_movie_by_id(movie_id, update_movie_data, expected_status=403)
        assert response.status_code == 403

    @pytest.mark.negative
    def test_post_movie_review_by_id_as_unauthorized(self, unauth_api_manager, create_movie, review_data):
        movie_id = create_movie['id']
        response = unauth_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data, expected_status=401)
        assert response.status_code == 401

    @pytest.mark.negative
    def test_update_movie_review_by_id_as_user(
            self, admin_api_manager, user_api_manager, create_movie, review_data, update_review_data
    ):
        movie_id = create_movie['id']

        admin_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)

        response = user_api_manager.movies_api.update_movie_review_by_id(movie_id, update_review_data, expected_status=404)
        # Должен быть 404 статус?
        assert response.status_code == 404

    @pytest.mark.negative
    def test_delete_movie_review_by_id_as_unauthorized(
            self, unauth_api_manager, user_api_manager, create_movie, review_data
    ):
        movie_id = create_movie['id']

        user_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)

        response = unauth_api_manager.movies_api.delete_movie_review_by_id(movie_id, expected_status=401)
        assert response.status_code == 401

    @pytest.mark.negative
    def test_delete_movie_admin_review_by_id_as_user(
            self, admin_api_manager, user_api_manager, create_movie, review_data
    ):
        movie_id = create_movie['id']

        admin_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)

        response = user_api_manager.movies_api.delete_movie_review_by_id(movie_id, expected_status=404)
        assert response.status_code == 404

    @pytest.mark.negative
    def test_hide_movie_review_by_id_as_user(self, user_api_manager, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = user_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        response = user_api_manager.movies_api.hide_movie_review_by_id(movie_id, user_id, expected_status=403)
        assert response.status_code == 403

    @pytest.mark.negative
    def test_show_movie_review_by_id_as_user(self, user_api_manager, admin_api_manager, create_movie, review_data):
        movie_id = create_movie['id']

        create_response = admin_api_manager.movies_api.post_movie_review_by_id(movie_id, review_data)
        user_id = create_response.json()['userId']

        admin_api_manager.movies_api.hide_movie_review_by_id(movie_id, user_id)

        response = user_api_manager.movies_api.show_movie_review_by_id(movie_id, user_id, expected_status=403)
        assert response.status_code == 403