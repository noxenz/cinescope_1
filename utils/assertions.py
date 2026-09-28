from pydantic import ValidationError
from pytest_check import check

def validate_response(model, movie_data: dict):
    try:
        model(**movie_data)
    except ValidationError as e:
        with check:
            assert False, f'Баг апи: {e}'