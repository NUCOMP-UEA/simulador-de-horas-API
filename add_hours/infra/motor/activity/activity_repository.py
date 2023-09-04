from datetime import datetime

from bson.objectid import ObjectId

from add_hours.domain.models.activity.activity import Activity
from add_hours.domain.models.activity.activity_type import ActivityType
from add_hours.domain.repository.activity_repository_interface import (
    IActivityRepository,
)
from add_hours.infra.motor.activity.activity_model import ActivityMotor
from add_hours.infra.motor.activity.activity_type_model import ActivityTypeMotor
from add_hours.infra.motor.student.student_repository import (
    StudentRepositoryMotor,
)


class ActivityRepositoryMotor(IActivityRepository):
    @classmethod
    async def save_activity(cls, activity: Activity):
        activity_db = ActivityMotor(
            **activity.model_dump(
                exclude={
                    "_id",
                    "id_",
                    "id",
                    "startDate",
                    "endDate",
                    "category",
                    "student",
                },
                by_alias=True,
            ),
            start_date=datetime(
                day=activity.start_date.day,
                month=activity.start_date.month,
                year=activity.start_date.year,
            ),
            end_date=datetime(
                day=activity.end_date.day,
                month=activity.end_date.month,
                year=activity.end_date.year,
            ),
            category=ObjectId(activity.category),
            student=ObjectId(activity.student)
        )

        if not activity_db.accomplished_workload:
            activity_db.accomplished_workload = activity_db.posted_workload

        await ActivityMotor.save_activity(activity_db)

    @classmethod
    async def category_limit_verifier(
        cls, activity: Activity, activity_type: ActivityType
    ):
        posted_workload = await cls._find_posted_workload(
            activity, activity_type
        )
        activity.posted_workload = posted_workload

        activity_pipeline = [
            {
                "$match": {
                    "student": ObjectId(activity.student),
                    "category": ObjectId(activity.category),
                }
            },
            {
                "$group": {
                    "_id": None,
                    "posted_workload": {"$sum": "$postedWorkload"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "posted_workload": {
                        "$sum": [
                            "$posted_workload",
                            activity.posted_workload,
                        ]
                    },
                }
            },
        ]

        new_posted_workload = await ActivityMotor.aggregate(activity_pipeline)

        if (
            new_posted_workload
            and new_posted_workload[0]["posted_workload"] > activity_type.limit
        ):
            return True
        return False

    @classmethod
    async def get_activities(
        cls, student_id: str, current_page: int, page_size: int
    ):
        activities_db, total_activities = await ActivityMotor.paginate_database(
            current_page=current_page, page_size=page_size
        )

        activity_total_posted_workload_pipeline = [
            {"$match": {"student": ObjectId(student_id)}},
            {
                "$group": {
                    "_id": "$category",
                    "total_posted_workload": {"$sum": "$postedWorkload"},
                }
            },
        ]

        total_posted_workload = await ActivityMotor.aggregate(
            pipeline=activity_total_posted_workload_pipeline
        )
        total_posted_workload = sum(
            total["total_posted_workload"] for total in total_posted_workload
        )

        activity_total_accomplished_workload_pipeline = [
            {"$match": {"student": ObjectId(student_id)}},
            {
                "$group": {
                    "_id": "$category",
                    "total_accomplished_workload": {
                        "$sum": "$accomplishedWorkload"
                    },
                }
            },
        ]
        total_accomplished_workload = await ActivityMotor.aggregate(
            pipeline=activity_total_accomplished_workload_pipeline
        )

        total_accomplished_workload = sum(
            total["total_accomplished_workload"]
            for total in total_accomplished_workload
        )

        if not total_posted_workload:
            total_posted_workload = 0
        if not total_accomplished_workload:
            total_accomplished_workload = 0

        if not activities_db:
            return [], 0
        return (
            activities_db,
            total_activities,
            total_posted_workload,
            total_accomplished_workload,
        )

    @classmethod
    async def _find_posted_workload(
        cls, activity: Activity, activity_type: ActivityType
    ):
        posted_workload = (
            activity_type.multiplying_factor * activity.accomplished_workload
            if activity_type.hours is None
            else activity_type.hours * activity.periods
            if activity_type.is_period_required is not False
            else activity_type.hours
        )
        posted_workload = (
            posted_workload
            if posted_workload <= activity_type.limit
            else activity_type.limit
        )
        return posted_workload
