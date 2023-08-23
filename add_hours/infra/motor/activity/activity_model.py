from datetime import datetime
from typing import Annotated, Optional

from bson.objectid import ObjectId
from pydantic import Field

from add_hours.infra.motor.database_setup import MotorBaseModel
from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityMotor(MotorBaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    activity: Annotated[ObjectId, PydanticObjectId]
    category: str
    area: str
    date_: datetime = Field(alias="date")
    accomplished_workload: Optional[int]
    posted_workload: Optional[int] = None

    class Config:
        populate_by_name = True
