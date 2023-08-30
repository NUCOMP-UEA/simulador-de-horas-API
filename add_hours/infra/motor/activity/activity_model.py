from datetime import datetime
from typing import Annotated, Optional

from bson.objectid import ObjectId
from pydantic import Field

from add_hours.infra.motor.database_setup import MotorBaseModel
from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityMotor(MotorBaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    student: Annotated[ObjectId, PydanticObjectId]
    activity: str
    institution: str
    category: Annotated[ObjectId, PydanticObjectId]
    area: str
    start_date: datetime = Field(alias="startDate")
    end_date: datetime = Field(alias="endDate")
    periods: Optional[int] = Field(default=None)
    accomplished_workload: Optional[int] = Field(alias="accomplishedWorkload")
    posted_workload: Optional[int] = Field(alias="postedWorkload")

    class Config:
        populate_by_name = True
