from datetime import date
from typing import Annotated, Optional

from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel

from add_hours.utils.camel_case import to_camel_case
from add_hours.utils.pydantic_object_id import PydanticObjectId


class Activity(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    student: Annotated[ObjectId, PydanticObjectId]
    activity: str
    institution: str
    category: Annotated[ObjectId, PydanticObjectId]
    area: str
    start_date: date
    end_date: date
    periods: Optional[int] = Field(default=None)
    accomplished_workload: Optional[int] = Field()
    posted_workload: Optional[int] = Field(default=None)

    class Config:
        populate_by_name = True
        alias_generator = to_camel_case
