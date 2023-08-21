from datetime import datetime, date
from enum import Enum

from pydantic import BaseModel, Field


class ActivityRequest(BaseModel):
    activity: str
    category: str
    area: str
    date_: date = Field(alias="date")
    accomplished_workload: int = Field(alias="accomplishedWorkload")
    posted_workload: int = Field(alias="postedWorkload")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "activity": "Activity 1",
                "category": "Category 1",
                "area": "Area 1",
                "date": datetime.utcnow().date(),
                "accomplishedWorkload": 80,
                "postedWorkload": 80,
            }
        }


class ActivityUpdateRequest(BaseModel):
    activity: str = None
    category: str = None
    area: str = None
    date: datetime = None
    accomplished_workload: int = Field(
        default=None, alias="accomplishedWorkload"
    )
    posted_workload: int = Field(default=None, alias="postedWorkload")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "activity": "Activity 1",
                "category": "Category 1",
                "area": "Area 1",
                "date": str(datetime.utcnow()),
                "accomplishedWorkload": 80,
                "postedWorkload": 80,
            }
        }


class DimensionEnum(str, Enum):
    teaching = "ENSINO"
    research = "PESQUISA"
    extension = "EXTENSÃO"
    others = "OUTROS"


class ActivityTypeRequest(BaseModel):
    activity_id: int = Field(alias="activityId")
    dimension: DimensionEnum
    activity_type: str = Field(alias="activityType")
    limit: int

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "activityId": 1,
                "dimension": DimensionEnum.teaching,
                "activityType": "Instrução de oficinas, palestras ou cursos de capacitação certificado pela entidade organizadora.",
                "limit": 40,
            }
        }
