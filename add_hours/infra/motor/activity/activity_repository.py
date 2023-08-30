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
                            {
                                "$cond": [
                                    {"$ne": ["$isPeriodRequired", False]},
                                    {
                                        "$multiply": [
                                            "$hours",
                                            activity_db.periods,
                                        ]
                                    },
                                    "$hours",
                                ]
                            },
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

        if activity_type_aggregation_result:
            activity_db.posted_workload = int(
                activity_type_aggregation_result[0]["posted_workload"]
            )

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
                        "limit": 1,
                        "postedWorkload": 1,
                    }
                },
            ]

            result_activity = await ActivityMotor.aggregate(activity_pipeline)
            if result_activity and result_activity[0]["result"] is False:
                activity_db.posted_workload = abs(
                    int(result_activity[0]["postedWorkload"])
                    - activity_db.posted_workload
                    - int(result_activity[0]["limit"])
                )

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

            # TODO: Refatorar daqui para baixo
            result_total_per_course = await ActivityMotor.aggregate(
                total_per_course_pipeline
            )

            if result_total_per_course and course_max < (
                int(result_total_per_course[0]["result"])
                + activity_db.posted_workload
            ):
                activity_db.posted_workload = abs(
                    course_max - int(result_total_per_course[0]["result"])
                )

            if not activity_db.accomplished_workload:
                activity_db.accomplished_workload = activity_db.posted_workload

            await ActivityMotor.save_activity(activity_db)
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
    async def activity_exists(cls, activity_id: str):
        return ActivityMotor.exists(_id=ObjectId(activity_id))
