from datetime import date, datetime
from typing import Annotated

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityResponse(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(
        examples=[str(ObjectId())], alias="_id"
    )
    activity: str = Field(example="Activity 1")
    category: str = Field(example="Category 1")
    area: str = Field(example="Area 1")
    date_: date = Field(example=datetime.utcnow().date(), alias="date")
    accomplished_workload: int = Field(alias="accomplishedWorkload", example=80)
    posted_workload: int = Field(alias="postedWorkload", example=80)

    class Config:
        json_encoders = {PydanticObjectId: lambda v: str(v)}
        populate_by_name = True
        arbitrary_types_allowed = True


class GetActivitiesResponse(BaseModel):
    total_activities: int = Field(alias="totalActivities", example=10)
    activities: list[ActivityResponse]

    class Config:
        populate_by_name = True
