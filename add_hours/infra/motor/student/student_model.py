from typing import Annotated

from bson.objectid import ObjectId
from pydantic import Field

from add_hours.infra.motor.database_setup import MotorBaseModel
from add_hours.utils.pydantic_object_id import PydanticObjectId


class StudentMotor(MotorBaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(alias="_id")
    name: str
    enrollment: str
    email: str
    course: str

    class Config:
        populate_by_name = True
