from typing import Annotated, Optional

from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel

from add_hours.utils.camel_case import to_camel_case
from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityType(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    id_and_dimension: str
    activity_type: str
    activity_type_response: str
    limit: int
    multiplying_factor: Optional[float]
    hours: Optional[int]
    is_period_required: bool

    class Config:
        populate_by_name = True
        alias_generator = to_camel_case
