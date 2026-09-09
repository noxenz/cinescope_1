import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles
from constants.locations import Locations

EMAIL_PATTERN = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

logger = logging.getLogger(__name__)

class TestUser(BaseModel):
    email: str = Field(..., pattern=EMAIL_PATTERN, description='Email пользователя')
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
    email: str = Field(..., pattern=EMAIL_PATTERN)
    fullName: str = Field(..., min_length=1, max_length=100)
    verified: bool
    roles: list[Roles]
    createdAt: datetime
    banned: bool

class GenreResponse(BaseModel):
    name: str

class MovieResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str]
    location: Locations
    published: bool
    genreId: int
    genre: GenreResponse
    createdAt: str
    rating: float = Field(ge=0)

def get_user(test_user):
    return test_user

def test_user_data(test_user):
    user = TestUser(**get_user(test_user))
    assert user.email == test_user['email']
    logger.info(f'{user.email} {user.fullName} {user.password} {user.passwordRepeat} {user.roles}')