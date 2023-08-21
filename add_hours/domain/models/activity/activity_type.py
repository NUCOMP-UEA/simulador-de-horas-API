from typing import Annotated

from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel

from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityType(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="id")
    activity_id: int = Field(alias="activityId")
    dimension: str
    activity_type: str = Field(alias="activityType")
    limit: int

    class Config:
        populate_by_name = True
