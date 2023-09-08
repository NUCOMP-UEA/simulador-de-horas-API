from passlib.context import CryptContext
from pydantic import BaseModel, SecretStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    password: SecretStr

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compare_passwords(self, input_password: SecretStr) -> bool:
        return pwd_context.verify(
            self.password.get_secret_value(),
            input_password.get_secret_value()
        )

    def change_to_hash(self):
        self.password = SecretStr(self.hash_password)
