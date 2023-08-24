from typing import Annotated

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from add_hours.utils.pydantic_object_id import PydanticObjectId


class Student(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    name: str
    enrollment: str
    email: str
    course: str

    class Config:
        populate_by_name = True
