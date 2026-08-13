"""Модели песочницы. Повторяют реальную структуру ответов Cinescope /movies."""
from datetime import datetime
from enum import Enum
from typing import Optional
from constants.roles import Roles

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, ValidationInfo

class BaseModelForbid(BaseModel):
    model_config = ConfigDict(strict=False)

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
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    fullName: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8, max_length=20)
    passwordRepeat: str = Field(..., min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator('passwordRepeat')
    def check_password_match(cls, value: str, info: ValidationInfo) -> str:
        password = info.data.get('password')
        if value != password:
            raise ValueError('Пароли не совпадают')
        return value

class Card(BaseModel):
    pan: str = Field(..., min_length=16, max_length=16)
    cvc: str = Field(..., min_length=3, max_length=4)

    @field_validator('pan')
    def check_pan_is_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError('PAN должен содержать только цифры')
        return value

class CardType(str, Enum):
    VISA = 'Visa'
    AMEX = 'American Express'

class TypeCard(BaseModel):
    pan: str = Field(..., min_length=16, max_length=16)
    cvc: str = Field(..., min_length=3, max_length=4)
    card_type: CardType

    @model_validator(mode='after')
    def check_cvc_length(self):
        expected = 3 if self.card_type == CardType.VISA else 4
        if len(self.cvc) != expected:
            raise ValueError(f'CVC для {self.card_type.value} должен быть {expected} цифры')
        return self