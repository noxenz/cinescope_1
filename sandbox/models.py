"""Модели песочницы. Повторяют реальную структуру ответов Cinescope /movies."""
from datetime import datetime
from enum import Enum
from typing import Optional
from constants.roles import Roles

from pydantic import BaseModel, Field, ConfigDict

class BaseModelForbid(BaseModel):
    model_config = ConfigDict(strict=True)

class Location(str, Enum):
    MSK = "MSK"
    SPB = "SPB"

# --- самые внутренние модели ---

class Genre(BaseModelForbid):
    """Жанр внутри фильма. Приходит как {"name": "Драма"}."""
    name: str
    id: Optional[int] = None

class ReviewUser(BaseModelForbid):
    """Автор отзыва. Приходит как {"fullName": "Melissa Ellis"}."""
    fullName: str

# --- средний уровень ---

class Review(BaseModelForbid):
    userId: str
    text: str
    rating: int = Field(..., ge=0, le=5)
    createdAt: datetime
    user: ReviewUser            # вложенная модель

class Movie(BaseModelForbid):
    id: int = Field(strict=True)
    name: str
    description: str
    genreId: int
    imageUrl: str
    price: int
    rating: float = Field(..., ge=0, le=5)
    location: Location
    published: bool
    createdAt: datetime
    genre: Genre                # вложенная модель

# --- то, что реально возвращают эндпоинты ---

class MoviesPage(BaseModelForbid):
    """Ответ GET /movies - страница со списком фильмов."""
    movies: list[Movie]         # список вложенных моделей
    count: int
    page: int
    pageSize: int
    pageCount: int

class MovieDetails(Movie):
    """Ответ GET /movies/{id} - тот же фильм, но ещё и с отзывами.

    Наследуемся от Movie, чтобы не переписывать 11 полей заново.
    """
    reviews: list[Review]

class TestUser(BaseModelForbid):
    email: str
    fullName: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8, max_length=20)
    passwordRepeat: str = Field(..., min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None