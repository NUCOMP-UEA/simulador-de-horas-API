from typing import Type

from add_hours.application.dto.request.activity import ActivityTypeRequest
from add_hours.domain.models.activity.activity_type import ActivityType
from add_hours.domain.repository.activity_type_repository_interface import (
    IActivityTypeRepository,
)


class ActivityTypeService:
    activity_type_repository: Type[IActivityTypeRepository]

    def __new__(cls, activity_repository: Type[IActivityTypeRepository]):
        cls.activity_type_repository = activity_repository
        return cls

    @classmethod
    async def save_activity_type(
        cls, activity_type_request: ActivityTypeRequest
    ):
        activity = ActivityType(**activity_type_request.model_dump())

        await cls.activity_type_repository.save_activity_type(activity)
