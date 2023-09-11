from typing import Type

from pydantic import SecretStr

from add_hours.application.exceptions.unauthorized import InvalidUser
from add_hours.application.security.IAuthRepository import IAuthRepository
from add_hours.domain.models.auth.user import User


class AuthService:
    auth_repository: Type[IAuthRepository]

    def __new__(cls, auth_repository: Type[IAuthRepository]):
        cls.auth_repository = auth_repository
        return cls

    @classmethod
    async def verify_user(cls, username: str, password: SecretStr):
        user = User(username=username, password=password)
        user_db_hashed_password: SecretStr = (
            await cls.auth_repository.get_user_hashed_password(username)
        )

        if not user_db_hashed_password:
            raise InvalidUser("Unauthorized user")

        return user.compare_passwords(user_db_hashed_password)
