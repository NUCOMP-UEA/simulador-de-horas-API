from typing import Annotated

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from add_hours.utils.pydantic_object_id import PydanticObjectId


class StudentResponse(BaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(
        examples=[str(ObjectId())], alias="_id"
    )
    name: str = Field(example="Lorem Ipsum")
    enrollment: str = Field(example="2015080001")
    email: str = Field(example="loremipsum@example.com")
    course: str = Field(example="ECP")

    class Config:
        json_encoders = {PydanticObjectId: lambda v: str(v)}
        populate_by_name = True
        arbitrary_types_allowed = True
