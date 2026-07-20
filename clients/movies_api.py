from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

MOVIES = '/movies'
REVIEWS = '/reviews'
HIDE = '/hide'
SHOW = '/show'

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_movies_list(self, expected_status=200, **kwargs):
        return self.send_request(
            method='GET',
            endpoint=MOVIES,
            expected_status=expected_status,
            **kwargs
        )

    def create_movie(self, movie_data, expected_status=201, **kwargs):
        return self.send_request(
            method='POST',
            endpoint=MOVIES,
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )

    def get_movie_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method='GET',
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status,
            **kwargs
        )

    def delete_movie_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method='DELETE',
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status,
            **kwargs
        )

    def update_movie_by_id(self, movie_id, update_movie_data, expected_status=200, **kwargs):
        return self.send_request(
            method='PATCH',
            endpoint=f'{MOVIES}/{movie_id}',
            data=update_movie_data,
            expected_status=expected_status,
            **kwargs
        )

    def get_movie_reviews_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method='GET',
            endpoint=f'{MOVIES}/{movie_id}{REVIEWS}',
            expected_status=expected_status,
            **kwargs
        )

    def post_movie_review_by_id(self, movie_id, review_data, expected_status=201, **kwargs):
        return self.send_request(
            method='POST',
            endpoint=f'{MOVIES}/{movie_id}{REVIEWS}',
            data=review_data,
            expected_status=expected_status,
            **kwargs
        )

    def update_movie_review_by_id(self, movie_id, review_data, expected_status=200, **kwargs):
        return self.send_request(
            method='PUT',
            endpoint=f'{MOVIES}/{movie_id}{REVIEWS}',
            data=review_data,
            expected_status=expected_status,
            **kwargs
        )

    def delete_movie_review_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method='DELETE',
            endpoint=f'{MOVIES}/{movie_id}{REVIEWS}',
            expected_status=expected_status,
            **kwargs
        )

    def hide_movie_review_by_id(self, movie_id, user_id, expected_status=200, **kwargs):
        return self.send_request(
            method='PATCH',
            endpoint=f'{MOVIES}/{movie_id}{REVIEWS}{HIDE}/{user_id}',
            expected_status=expected_status,
            **kwargs
        )

    def show_movie_review_by_id(self, movie_id, user_id, expected_status=200, **kwargs):
        return self.send_request(
            method='PATCH',
            endpoint=f'{MOVIES}/{movie_id}{REVIEWS}{SHOW}/{user_id}',
            expected_status=expected_status,
            **kwargs
        )