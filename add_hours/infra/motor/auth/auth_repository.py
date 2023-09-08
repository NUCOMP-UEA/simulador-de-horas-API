from pydantic import SecretStr

from add_hours.application.security.IAuthRepository import IAuthRepository
from add_hours.infra.motor.user.user_model import UserMotor


class AuthRepositoryMotor(IAuthRepository):

    @classmethod
    async def get_user_hashed_password(cls, username: str) -> SecretStr | None:
        password = await UserMotor.find_one(username=username)
        if password:
            return SecretStr(password.get("password"))
