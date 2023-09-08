from typing import Annotated

from bson.objectid import ObjectId
from pydantic import Field, SecretStr

from add_hours.infra.motor.database_setup import MotorBaseModel
from add_hours.utils.pydantic_object_id import PydanticObjectId


class UserMotor(MotorBaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(alias="_id")
    username: str
    password: SecretStr

    class Config:
        populate_by_name = True
