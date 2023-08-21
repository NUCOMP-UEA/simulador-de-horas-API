from typing import Annotated

from bson.objectid import ObjectId
from pydantic import Field

from add_hours.infra.motor.database_setup import MotorBaseModel
from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityTypeMotor(MotorBaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    activity_id: int = Field(alias="activityId")
    dimension: str
    activity_type: str = Field(alias="activityType")
    limit: int

    class Config:
        populate_by_name = True
