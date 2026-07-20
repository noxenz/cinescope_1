from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

GENRES = '/genres'

class GenresApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_genres(self, expected_status=200, **kwargs):
        return self.send_request(
            method='GET',
            endpoint=GENRES,
            expected_status=expected_status,
            **kwargs
        )