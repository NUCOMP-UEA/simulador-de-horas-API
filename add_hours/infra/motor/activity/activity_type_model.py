from typing import Annotated, Optional

from bson.objectid import ObjectId
from pydantic import Field

from add_hours.infra.motor.database_setup import MotorBaseModel
from add_hours.utils.pydantic_object_id import PydanticObjectId


class ActivityTypeMotor(MotorBaseModel):
    id_: Annotated[ObjectId, PydanticObjectId] = Field(default=None, alias="_id")
    id_and_dimension: str = Field(alias="idAndDimension")
    activity_type: str = Field(alias="activityType")
    activity_type_response: str = Field(alias="activityTypeResponse")
    limit: int
    multiplying_factor: Optional[float] = Field(alias="multiplyingFactor")
    hours: Optional[int]
    is_period_required: bool = Field(alias="isPeriodRequired")

    class Config:
        populate_by_name = True
