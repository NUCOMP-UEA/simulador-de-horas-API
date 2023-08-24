from typing import Annotated, Optional

from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel

from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityType(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    id_and_dimension: str = Field(alias="idAndDimension")
    activity_type: str = Field(alias="activityType")
    limit: int
    multiplying_factor: Optional[float] = Field(alias="multiplyingFactor")
    hours: Optional[int]

    class Config:
        populate_by_name = True
