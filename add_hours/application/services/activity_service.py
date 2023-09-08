from typing import Optional, Type

from bson.objectid import ObjectId
from fastapi import HTTPException

from add_hours.application.dto.request.activity import (
    ActivityRequest,
)
from add_hours.application.dto.response.activity import (
    ActivityResponse,
    ActivitySaveResponse, GetActivitiesResponse,
)
from add_hours.application.services.activity_type_service import (
    ActivityTypeService,
)
from add_hours.application.services.student_service import StudentService
from add_hours.domain.models.activity.activity import Activity
from add_hours.domain.models.activity.activity_type import ActivityType
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
        if not ObjectId.is_valid(
                activity_request.category
        ) or not ObjectId.is_valid(activity_request.student):
            # TODO: Exception temporária
            raise HTTPException(status_code=422, detail="Invalid object id")

        if activity_request.start_date > activity_request.end_date:
            # TODO: Excessão temporária
            raise HTTPException(
                status_code=400,
                detail="Incoherent date: start date is greater than end date",
            )

        activity_type_exists = await ActivityTypeService.activity_type_exists(
            str(activity_request.category)
        )
        if not activity_type_exists:
            # TODO: Excessão temporária
            raise HTTPException(
                status_code=404,
                detail="Activity Category not found",
            )
        activity_type = ActivityType(**activity_type_exists)

        activity_id = ObjectId()
        activity = Activity(**activity_request.model_dump(), id_=activity_id)

        if (
                activity_type.hours is None
                and activity.accomplished_workload is None
        ):
            # TODO: Excessão temporária
            raise HTTPException(
                status_code=400,
                detail="Accomplished workload should not be None while the fixed"
                       " hours for this category is also None",
            )

        if activity_type.is_period_required is None and not activity.periods:
            # TODO: Excessão temporária
            raise HTTPException(
                status_code=400,
                detail="Invalid field periods for this Activity Category, "
                       "periods field is required",
            )

        student_exists = await StudentService.get_student(str(activity.student))

        if not student_exists:
            raise HTTPException(
                status_code=404, detail="The given student id does not exist"
            )

        is_greater_than_limit = (
            await cls.activity_repository.category_limit_verifier(
                activity, activity_type
            )
        )

        if is_greater_than_limit:
            # TODO: Excessão temporária
            raise HTTPException(
                status_code=400,
                detail="Workload is greater than the Category limit",
            )

        await cls.activity_repository.save_activity(activity)

        return ActivitySaveResponse(id_=activity_id)

    @classmethod
    async def get_activities(
        cls,
        student_id: str,
        current_page: Optional[int],
        page_size: Optional[int],
    ) -> GetActivitiesResponse:
        if not ObjectId.is_valid(student_id):
            # TODO: Exception temporária
            raise HTTPException(status_code=422, detail="Invalid student id")

        current_page = 1 if current_page is None else current_page
        page_size = 10 if page_size is None else page_size
        (
            response,
            total_activities,
            total_posted_workload,
            total_accomplished_workload,
        ) = await cls.activity_repository.get_activities(
            student_id, current_page, page_size
        )

        return GetActivitiesResponse(
            total_activities=total_activities,
            activities=[ActivityResponse(**activity) for activity in response],
            total_posted_workload=total_posted_workload,
            total_accomplished_workload=total_accomplished_workload,
        )

    @classmethod
    def delete_activity(cls, activity_id: str):
        if not ObjectId.is_valid(activity_id):
            # TODO: Exception temporária
            raise HTTPException(status_code=422, detail="Invalid activity id")

    @classmethod
    async def activity_exists(cls, activity_id: str):
        if not ObjectId.is_valid(activity_id):
            # TODO: Exception temporária
            raise HTTPException(status_code=422, detail="Invalid activity id")

        return await cls.activity_repository.activity_exists(activity_id)
