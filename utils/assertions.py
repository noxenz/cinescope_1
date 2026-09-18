from pydantic import ValidationError
from pytest_check import check
from models.base_models import MovieResponse

def validate_movies_response(movies: list[dict]):
    for movie_data in movies:
        try:
            MovieResponse(**movie_data)
        except ValidationError as e:
            with check:
                assert False, f'Баг апи: {e}'

def validate_movie_response(movie_data: dict):
    try:
        MovieResponse(**movie_data)
    except ValidationError as e:
        with check:
            assert False, f'Баг апи: {e}'