"""Модели песочницы. Повторяют реальную структуру ответов Cinescope /movies."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

class Location(str, Enum):
    MSK = "MSK"
    SPB = "SPB"

# --- самые внутренние модели ---

class Genre(BaseModel):
    """Жанр внутри фильма. Приходит как {"name": "Драма"}."""
    name: str

class ReviewUser(BaseModel):
    """Автор отзыва. Приходит как {"fullName": "Melissa Ellis"}."""
    fullName: str

# --- средний уровень ---

class Review(BaseModel):
    userId: str
    text: str
    rating: int = Field(..., ge=0, le=5)
    createdAt: datetime
    user: ReviewUser            # вложенная модель

class Movie(BaseModel):
    id: int
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

class MoviesPage(BaseModel):
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