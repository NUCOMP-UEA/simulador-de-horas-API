from typing import Optional, Type, Union

from bson.objectid import ObjectId
from fastapi import HTTPException

from add_hours.application.dto.request.activity import (
    ActivityRequest,
    ActivityUpdateRequest,
)
from add_hours.application.dto.response.activity import (
    ActivityResponse,
    ActivitySaveResponse,
    GetActivitiesResponse,
)
from add_hours.application.exceptions.bad_request import (
    IncoherentDateBadRequest,
    IncoherentFieldBadRequestDatabase,
)
from add_hours.application.exceptions.not_found import (
    ActivityNotFoundInDatabase,
    ActivityTypeNotFoundInDatabase,
    StudentNotFoundInDatabase,
)
from add_hours.application.exceptions.unprocessable_entity import (
    InvalidIdUnprocessableEntityDatabase,
)
from add_hours.application.services.activity_type_service import (
    ActivityTypeService,
)
from add_hours.application.services.storage_service import StorageService
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
            raise InvalidIdUnprocessableEntityDatabase("Invalid object id")

        activity = await cls._do_pipelines(activity_request)

        await cls.activity_repository.save_activity(activity)

        return ActivitySaveResponse(id_=activity.id_)

    @classmethod
    async def get_activities(
        cls,
        student_id: str,
        current_page: Optional[int],
        page_size: Optional[int],
    ) -> GetActivitiesResponse:
        if not ObjectId.is_valid(student_id):
            raise InvalidIdUnprocessableEntityDatabase("Invalid student id")

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
    async def delete_activity(cls, student_id: str, activity_id: str):
        student_exists = await StudentService.student_exists(student_id)

        if not student_exists:
            raise StudentNotFoundInDatabase()

        activity_exists = await cls.activity_exists(activity_id)

        if not activity_exists:
            raise ActivityNotFoundInDatabase()

        await cls.activity_repository.delete_activity(student_id, activity_id)
        await StorageService.remove_certificate(student_id, activity_id)

    @classmethod
    async def activity_exists(cls, activity_id: str):
        if not ObjectId.is_valid(activity_id):
            raise InvalidIdUnprocessableEntityDatabase("Invalid activity id")

        return await cls.activity_repository.activity_exists(activity_id)

    @classmethod
    async def get_activity(cls, activity_id: str):
        return ActivityResponse(
            **(await cls.activity_repository.get_activity(activity_id))
        )

    @classmethod
    async def update_activity(
        cls,
        student_id: str,
        activity_id: str,
        update_request: ActivityUpdateRequest,
    ):
        student_exists = await StudentService.student_exists(student_id)

        if not student_exists:
            raise StudentNotFoundInDatabase()

        activity_exists = await cls.activity_exists(activity_id)

        if not activity_exists:
            raise ActivityNotFoundInDatabase()

        update_request.student = student_id
        update_request.id_ = activity_id

        activity = await cls._do_pipelines(update_request)

        await cls.activity_repository.update_activity(activity)

        await StorageService.remove_certificate(student_id, activity_id)

    @classmethod
    async def _do_pipelines(
        cls, request: Union[ActivityRequest, ActivityUpdateRequest]
    ):
        if request.start_date > request.end_date:
            raise IncoherentDateBadRequest(
                "Incoherent date: start date is greater than end date"
            )

        activity_type_exists = await ActivityTypeService.activity_type_exists(
            str(request.category)
        )
        if not activity_type_exists:
            raise ActivityTypeNotFoundInDatabase()

        activity_type = ActivityType(**activity_type_exists)

        if isinstance(request, ActivityRequest):
            activity_id = ObjectId()
            activity = Activity(**request.model_dump(), id_=activity_id)
        else:
            activity = Activity(**request.model_dump())

        if (
            activity_type.hours is None
            and activity.accomplished_workload is None
        ):
            raise IncoherentFieldBadRequestDatabase(
                "Accomplished workload should not be None while the fixed"
                " hours for this category is also None",
            )

        if activity_type.is_period_required is None and not activity.periods:
            raise IncoherentFieldBadRequestDatabase(
                "Invalid field periods for this Activity Category, "
                "periods field is required",
            )

        student_exists = await StudentService.get_student(str(activity.student))

        if not student_exists:
            raise StudentNotFoundInDatabase()

        is_greater_than_limit = (
            await cls.activity_repository.category_limit_verifier(
                activity, activity_type
            )
        )

        if is_greater_than_limit:
            raise IncoherentFieldBadRequestDatabase(
                "Workload is greater than the Category limit",
            )

        return activity
