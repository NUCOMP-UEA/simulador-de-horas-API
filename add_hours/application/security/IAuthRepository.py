from abc import ABC, abstractmethod

from pydantic import SecretStr


class IAuthRepository(ABC):
    @classmethod
    @abstractmethod
    async def get_user_hashed_password(cls, username: str) -> SecretStr | None:
        raise NotImplementedError()
