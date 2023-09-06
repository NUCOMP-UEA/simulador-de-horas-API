from typing import Type


class AuthService:
    auth_repository: Type[IAuthRepository]

    def __new__(cls, auth_repository: Type[IAuthRepository]):
        cls.auth_repository = auth_repository
        return cls
