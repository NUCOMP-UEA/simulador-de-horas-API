from typing import Optional, Type

from unidecode import unidecode

from add_hours.application.dto.request.activity import ActivityTypeRequest
from add_hours.application.dto.response.activity import (
    ActivityTypeSearchResponse,
)
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
        activity_type_response = activity_type_request.activity_type
        activity_type_request.activity_type = unidecode(
            activity_type_request.activity_type.lower()
        )

        activity = ActivityType(
            **activity_type_request.model_dump(by_alias=True),
            activity_type_response=activity_type_response
        )

        await cls.activity_type_repository.save_activity_type(activity)

    @classmethod
    async def search_activity_type(cls, search: Optional[str]):
        return [
            ActivityTypeSearchResponse(**search_result)
            for search_result in (
                await cls.activity_type_repository.search_activity_type(search)
            )
        ]

    @classmethod
    async def update_activity_type(
        cls, activity_type_request: ActivityTypeRequest
    ):
        activity = ActivityType(
            **activity_type_request.model_dump(by_alias=True)
        )
