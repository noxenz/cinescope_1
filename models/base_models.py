import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles

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
        """passwordRepeat обязан совпадать с password."""
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("passwordRepeat не совпадает с password")
        return value

class RegisterUserResponse(BaseModel):
    """Ответ на POST /register и POST /user."""

    id: str
    email: str = Field(..., pattern=EMAIL_PATTERN)
    fullName: str = Field(..., min_length=1, max_length=100)
    verified: bool
    roles: list[Roles]
    createdAt: datetime

def get_user(test_user):
    return test_user

def test_user_data(test_user):
    user = TestUser(**get_user(test_user))
    assert user.email == test_user['email']
    logger.info(f'{user.email} {user.fullName} {user.password} {user.passwordRepeat} {user.roles}')