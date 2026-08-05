import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[str]

def get_user(test_user):
    return test_user

def test_user_data(test_user):
    user = TestUser(**get_user(test_user))
    assert user.email == test_user['email']
    logger.info(f'{user.email} {user.fullName} {user.password} {user.passwordRepeat} {user.roles}')