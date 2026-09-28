import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, EmailStr

from constants.roles import Roles
from constants.locations import Locations

logger = logging.getLogger(__name__)

class TestUser(BaseModel):
    email: EmailStr
    fullName: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=20)
    passwordRepeat: str = Field(..., min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("passwordRepeat не совпадает с password")
        return value

class RegisterUserResponse(BaseModel):
    id: str = Field(..., description='UUID пользователя')
    email: EmailStr
    fullName: str = Field(..., min_length=1, max_length=100)
    verified: bool
    roles: list[Roles]
    createdAt: datetime
    banned: bool

class GenreResponse(BaseModel):
    id: int
    name: str

class MovieResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: Locations
    published: bool
    genreId: int
    genre: GenreResponse
    createdAt: str
    rating: float = Field(ge=0)

class FindAllMoviesResponse(BaseModel):
    movies: list[MovieResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int

class MovieReviewUserResponse(BaseModel):
    fullName: str

class MovieReviewResponse(BaseModel):
    userId: str
    rating: float = Field(ge=0)
    text: str
    createdAt: str
    user: MovieReviewUserResponse

class FindOneMovieResponse(MovieResponse):
    reviews: list[MovieReviewResponse]