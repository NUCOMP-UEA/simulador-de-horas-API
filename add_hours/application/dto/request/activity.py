from datetime import date, datetime, timedelta
from enum import Enum
from typing import Annotated, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityRequest(BaseModel):
    student: Annotated[ObjectId, PydanticObjectId]
    activity_type: Annotated[ObjectId, PydanticObjectId] = Field(
        alias="activityType"
    )
    category: str
    area: str
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    accomplished_workload: Optional[int] = Field(alias="accomplishedWorkload")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "student": "64e5278b82fc786f979af7f0",
                "activity": "64e5278b82fc786f979af7f0",
                "category": "Category 1",
                "area": "Area 1",
                "startDate": datetime.utcnow().date() - timedelta(days=1),
                "endDate": datetime.utcnow().date(),
                "accomplishedWorkload": 10,
            }
        }


class ActivityTypeRequest(BaseModel):
    id_and_dimension: str = Field(alias="idAndDimension")
    activity_type: str = Field(alias="activityType")
    activity_type_response: str = Field(alias="activityTypeResponse")
    limit: int
    multiplying_factor: Optional[float] = Field(alias="multiplyingFactor")
    hours: Optional[int]

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "idAndDimension": "1 - Ensino",
                "activityType": "Instrução de oficinas, palestras ou cursos de capacitação certificado pela entidade organizadora.",
                "limit": 40,
                "multiplyingFactor": 2.0,
                "hours": 0,
            }
        }
