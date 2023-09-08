from datetime import date, datetime, timedelta
from typing import Annotated, Optional

from bson import ObjectId
from pydantic import BaseModel, PositiveFloat, PositiveInt

from add_hours.utils.camel_case import to_camel_case
from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityRequest(BaseModel):
    student: Annotated[ObjectId, PydanticObjectId]
    activity: str
    institution: str
    category: Annotated[ObjectId, PydanticObjectId]
    area: str
    start_date: date
    end_date: date
    periods: Optional[PositiveInt]
    accomplished_workload: Optional[PositiveInt]

    class Config:
        populate_by_name = True
        alias_generator = to_camel_case
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
    id_and_dimension: str
    activity_type: str
    limit: PositiveInt
    multiplying_factor: Optional[PositiveFloat]
    hours: Optional[PositiveInt]
    is_period_required: bool

    class Config:
        populate_by_name = True
        alias_generator = to_camel_case
        json_schema_extra = {
            "example": {
                "idAndDimension": "1 - Ensino",
                "activityType": "Instrução de oficinas, palestras ou cursos de "
                                "capacitação certificado pela entidade "
                                "organizadora.",
                "limit": 40,
                "multiplyingFactor": 2.0,
                "hours": 0,
                "isPeriodRequired": False,
            }
        }
