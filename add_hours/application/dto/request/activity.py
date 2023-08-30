from datetime import date, datetime, timedelta
from typing import Annotated, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt

from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityRequest(BaseModel):
    student: Annotated[ObjectId, PydanticObjectId]
    activity: str
    institution: str
    category: Annotated[ObjectId, PydanticObjectId]
    area: str
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    periods: Optional[PositiveInt] = Field(default=None)
    accomplished_workload: Optional[PositiveInt] = Field(
        alias="accomplishedWorkload"
    )

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "student": "64e5278b82fc786f979af7f0",
                "activity": "Activity 1",
                "institution": "Institution 1",
                "category": "64e5278b82fc786f979af7f0",
                "area": "Area 1",
                # TODO: Validar se as datas estão corretas
                "startDate": datetime.utcnow().date() - timedelta(days=1),
                "endDate": datetime.utcnow().date(),
                "periods": 1,
                "accomplishedWorkload": 10,
            }
        }


class ActivityTypeRequest(BaseModel):
    id_and_dimension: str = Field(alias="idAndDimension")
    activity_type: str = Field(alias="activityType")
    limit: PositiveInt
    multiplying_factor: Optional[PositiveFloat] = Field(
        alias="multiplyingFactor"
    )
    hours: Optional[PositiveInt]
    is_period_required: bool = Field(alias="isPeriodRequired")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "idAndDimension": "1 - Ensino",
                "activityType": "Instrução de oficinas, palestras ou cursos de capacitação certificado pela entidade organizadora.",
                "limit": 40,
                "multiplyingFactor": 2.0,
                "hours": 0,
                "isPeriodRequired": False,
            }
        }
