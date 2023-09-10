from typing import Optional, Type

from bson.objectid import ObjectId
from fastapi import HTTPException
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

        activity_type = ActivityType(
            **activity_type_request.model_dump(by_alias=True),
            activity_type_response=activity_type_response
        )

        await cls.activity_type_repository.save_activity_type(activity_type)

    @classmethod
    async def search_activity_type(cls, search: Optional[str]):
        return [
            ActivityTypeSearchResponse(**search_result)
            for search_result in (
                await cls.activity_type_repository.search_activity_type(search)
            )
        ]

    @classmethod
    async def get_activity_type_by_id(cls, activity_type_id: str):
        return ActivityTypeSearchResponse(
            **(await cls.activity_type_repository.get_activity_type_by_id(
                activity_type_id
            ))
        )

    @classmethod
    async def update_activity_type(
        cls, activity_type_id: str, activity_type_request: ActivityTypeRequest
    ):
        if not ObjectId.is_valid(activity_type_id):
            # TODO: Excessão temporária
            raise HTTPException(status_code=422, detail="Invalid object id")

        activity_type_response = activity_type_request.activity_type
        activity_type_request.activity_type = unidecode(
            activity_type_request.activity_type.lower()
        )

        activity_type = ActivityType(
            **activity_type_request.model_dump(by_alias=True),
            activity_type_response=activity_type_response
        )

        await cls.activity_type_repository.update_activity_type(
            activity_type_id, activity_type
        )

    @classmethod
    async def activity_type_exists(cls, activity_type_id: str):
        return await cls.activity_type_repository.activity_type_exists(
            activity_type_id
        )

    @classmethod
    async def delete_activity_type(cls, activity_type_id: str):
        if not ObjectId.is_valid(activity_type_id):
            # TODO: Excessão temporária
            raise HTTPException(status_code=422, detail="Invalid object id")

        await cls.activity_type_repository.delete_activity_type(
            activity_type_id
        )
