from datetime import date, datetime, timedelta
from typing import Annotated

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivitySaveResponse(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(
        examples=[str(ObjectId())], alias="_id"
    )

    class Config:
        populate_by_name = True


class ActivityResponse(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(
        examples=[str(ObjectId())], alias="_id"
    )
    student: Annotated[ObjectId, PydanticObjectId] = Field(
        example="64e5278b82fc786f979af7f0Zz"
    )
    activity: str = Field(example="Activity 1")
    institution: str = Field(example="Institution 1")
    category: Annotated[ObjectId, PydanticObjectId] = Field(
        example="64e5278b82fc786f979af7f0"
    )
    area: str = Field(example="Area 1")
    start_date: date = Field(
        alias="startDate", example=datetime.utcnow().date() - timedelta(days=1)
    )
    end_date: date = Field(alias="endDate", example=datetime.utcnow().date())
    accomplished_workload: int = Field(alias="accomplishedWorkload", example=80)
    posted_workload: int = Field(alias="postedWorkload", example=80)

    class Config:
        json_encoders = {PydanticObjectId: lambda v: str(v)}
        populate_by_name = True
        arbitrary_types_allowed = True


class GetActivitiesResponse(BaseModel):
    total_activities: int = Field(alias="totalActivities", example=10)
    activities: list[ActivityResponse]
    total_posted_workload: int = Field(alias="totalPostedWorkload", example=80)
    total_accomplished_workload: int = Field(
        alias="totalAccomplishedWorkload", example=80
    )

    class Config:
        populate_by_name = True


class ActivityTypeSearchResponse(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(
        examples=[str(ObjectId())], alias="_id"
    )
    id_and_dimension: str = Field(alias="idAndDimension", example="1 - Ensino")
    activity_type: str = Field(
        alias="activityType", example="Activity type example"
    )
    is_period_required: bool = Field(alias="isPeriodRequired", example=False)

    class Config:
        populate_by_name = True
