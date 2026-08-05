import logging
from constants.roles import Roles
from typing import Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class TestUser(BaseModel):
    email: str
    fullName: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8, max_length=20)
    passwordRepeat: str = Field(..., min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

def get_user(test_user):
    return test_user

def test_user_data(test_user):
    user = TestUser(**get_user(test_user))
    assert user.email == test_user['email']
    logger.info(f'{user.email} {user.fullName} {user.password} {user.passwordRepeat} {user.roles}')