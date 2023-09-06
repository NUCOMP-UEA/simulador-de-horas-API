from passlib.context import CryptContext
from pydantic import BaseModel, SecretStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    password: SecretStr

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.change_to_hash()

    @property
    def hash_password(self):
        return pwd_context.hash(self.password.get_secret_value())

    def compare_passwords(self, input_password: str) -> bool:
        return pwd_context.verify(
            input_password, self.password.get_secret_value()
        )

    def change_to_hash(self):
        self.password = SecretStr(self.hash_password)
