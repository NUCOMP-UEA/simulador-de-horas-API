from datetime import datetime

from bson.objectid import ObjectId

from add_hours.domain.models.activity.activity import Activity
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

        activity_type_pipeline = [
            {"$match": {"_id": ObjectId(activity_db.category)}},
            {
                "$addFields": {
                    "posted_workload": {
                        "$cond": [
                            {"$eq": ["$hours", None]},
                            {
                                "$multiply": [
                                    "$multiplyingFactor",
                                    activity_db.accomplished_workload,
                                ]
                            },
                            "$hours",
                        ]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "posted_workload": {
                        "$cond": [
                            {"$lte": ["$posted_workload", "$limit"]},
                            "$posted_workload",
                            "$limit",
                        ]
                    },
                }
            },
        ]

        activity_type_aggregation_result = await ActivityTypeMotor.aggregate(
            activity_type_pipeline
        )

        if activity_type_aggregation_result is not None:
            activity_db.posted_workload = activity_type_aggregation_result[0][
                "posted_workload"
            ]

            activity_pipeline = [
                {
                    "$match": {
                        "student": ObjectId(activity_db.student),
                        "category": ObjectId(activity_db.category),
                    }
                },
                {
                    "$lookup": {
                        "from": "activitytype",
                        "localField": "category",
                        "foreignField": "_id",
                        "as": "limit",
                        "pipeline": [{"$project": {"_id": 0, "limit": 1}}],
                    }
                },
                {"$unwind": "$limit"},
                {
                    "$project": {
                        "_id": 0,
                        "limit": "$limit.limit",
                        "postedWorkload": 1,
                    }
                },
                {
                    "$group": {
                        "_id": "$limit",
                        "postedWorkload": {"$sum": "$postedWorkload"},
                    }
                },
                {
                    "$project": {
                        "limit": "$_id",
                        "postedWorkload": {
                            "$sum": [
                                "$postedWorkload",
                                activity_db.posted_workload,
                            ]
                        },
                    }
                },
                {
                    "$project": {
                        "result": {
                            "$cond": [
                                {
                                    "$lte": [
                                        "$postedWorkload",
                                        "$limit",
                                    ]
                                },
                                True,
                                False,
                            ]
                        },
                        "_id": 0,
                    }
                },
            ]

            student = await StudentRepositoryMotor.get_student(
                str(activity_db.student)
            )

            course_max = 0
            if student:
                course = student["course"]

                if course == "ECP":
                    course_max = 120
                elif course == "SI":
                    course_max = 180
                else:
                    course_max = 200
            else:
                return False

            total_per_course_pipeline = [
                {
                    "$match": {
                        "student": ObjectId(activity_db.student),
                    }
                },
                {"$group": {"_id": None, "total": {"$sum": "$postedWorkload"}}},
                {"$project": {"_id": 0, "result": "$total"}},
            ]

            result_activity = await ActivityMotor.aggregate(activity_pipeline)
            result_total_per_course = await ActivityMotor.aggregate(
                total_per_course_pipeline
            )

            if result_total_per_course and course_max <= (
                result_total_per_course[0]["result"]
                + activity_db.posted_workload
            ):
                new_posted_workload = (
                    (
                        activity_db.posted_workload
                        + result_total_per_course[0]["result"]
                        - course_max
                    )
                    if result_total_per_course[0]["result"] != course_max
                    else 0
                )
                activity_db.posted_workload = new_posted_workload

            if result_activity and result_activity[0]["result"] is False:
                return False

            await ActivityMotor.save_activity(activity_db)
            return True
        return False

    @classmethod
    async def get_activities(cls, current_page: int, page_size: int):
        activities_db, total_activities = await ActivityMotor.paginate_database(
            current_page=current_page, page_size=page_size
        )

        if not activities_db:
            return [], 0
        return activities_db, total_activities

    @classmethod
    async def activity_exists(cls, activity_id: str):
        return ActivityMotor.exists(_id=ObjectId(activity_id))
