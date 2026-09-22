from pydantic import ValidationError
from pytest_check import check
from models.base_models import MovieResponse, FindOneMovieResponse, FindAllMoviesResponse

def validate_movies_response(movie_data: dict):
        try:
            FindAllMoviesResponse(**movie_data)
        except ValidationError as e:
            with check:
                assert False, f'Баг апи: {e}'

def validate_movie_response(movie_data: dict):
    try:
        FindOneMovieResponse(**movie_data)
    except ValidationError as e:
        with check:
            assert False, f'Баг апи: {e}'

def validate_created_or_updated_movie(movie_data: dict):
    try:
        MovieResponse(**movie_data)
    except ValidationError as e:
        with check:
            assert False, f'Баг апи: {e}'