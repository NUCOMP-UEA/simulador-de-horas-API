from datetime import date
from typing import Annotated

from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel

from add_hours.utils.pydantic_object_id import PydanticObjectId


class Activity(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="id")
    activity: str
    category: str
    area: str
    date_: date = Field(alias="date")
    accomplished_workload: int = Field(alias="accomplishedWorkload")
    posted_workload: int = Field(alias="postedWorkload")

    class Config:
        populate_by_name = True
