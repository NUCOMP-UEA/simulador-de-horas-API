from typing import Optional, Type

from fastapi import HTTPException

from add_hours.application.dto.request.activity import (
    ActivityRequest,
)
from add_hours.application.dto.response.activity import (
    ActivityResponse,
    GetActivitiesResponse,
)
from add_hours.domain.models.activity.activity import Activity
from add_hours.domain.repository.activity_repository_interface import (
    IActivityRepository,
)


class ActivityService:
    activity_repository: Type[IActivityRepository]

    def __new__(cls, activity_repository: Type[IActivityRepository]):
        cls.activity_repository = activity_repository
        return cls

    @classmethod
    async def save_activity(cls, activity_request: ActivityRequest):
        activity = Activity(**activity_request.model_dump())

        response = await cls.activity_repository.save_activity(activity)

        if not response:
            # TODO: Excessão temporária
            raise HTTPException(
                status_code=400,
                detail="Activity was not added due to surpassing limit",
            )

    @classmethod
    async def get_activities(
        cls, current_page: Optional[int], page_size: Optional[int]
    ) -> GetActivitiesResponse:
        current_page, page_size = await cls._parse_paginate_params(
            current_page, page_size
        )

        (
            response,
            total_activities,
        ) = await cls.activity_repository.get_activities(current_page, page_size)

        return GetActivitiesResponse(
            total_activities=total_activities,
            activities=[ActivityResponse(**activity) for activity in response],
        )

    @classmethod
    def delete_activity(cls, activity_id: str):
        pass

    @classmethod
    async def _parse_paginate_params(
        cls, current_page: Optional[int], page_size: Optional[int]
    ):
        if page_size is None or page_size < 0:
            page_size = 10
        if current_page is None or current_page < 1:
            current_page = 1

        return [current_page, page_size]
