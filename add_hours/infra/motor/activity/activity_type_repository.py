import re

from bson.objectid import ObjectId
from unidecode import unidecode

from add_hours.domain.models.activity.activity_type import ActivityType
from add_hours.domain.repository.activity_type_repository_interface import (
    IActivityTypeRepository,
)
from add_hours.infra.motor.activity.activity_type_model import ActivityTypeMotor


class ActivityTypeRepositoryMotor(IActivityTypeRepository):
    @classmethod
    async def activity_type_exists(cls, activity_type_id: str):
        activity_type_db = await ActivityTypeMotor.find_one(
            _id=ObjectId(activity_type_id)
        )

        if not activity_type_db:
            return False
        return activity_type_db

    @classmethod
    async def save_activity_type(cls, activity_type: ActivityType):
        activity_type_db = ActivityTypeMotor(
            **activity_type.model_dump(
                exclude={"_id", "id_", "id"}, by_alias=True
            )
        )
        await activity_type_db.save()

    @classmethod
    async def search_activity_type(cls, search: str) -> list[dict]:
        if search is None:
            search = ""
        else:
            search = re.escape(unidecode(search.lower()))

        pipeline = [
            {
                "$addFields": {
                    "search_result": {
                        "$regexMatch": {
                            "input": "$activityType",
                            "regex": f"(.*?){search}(.*)",
                            "options": "i",
                        }
                    }
                }
            },
            {"$match": {"search_result": True}},
            {
                "$project": {
                    "_id": 1,
                    "id_and_dimension": "$idAndDimension",
                    "activity_type": "$activityTypeResponse",
                }
            },
        ]

        return await ActivityTypeMotor.aggregate(pipeline)

    @classmethod
    async def get_activity_type_by_id(cls, activity_type_id: str):
        pipeline = [
            {"$match": {"_id": ObjectId(activity_type_id)}},
            {
                "$project": {
                    "_id": 1,
                    "id_and_dimension": "$idAndDimension",
                    "activity_type": "$activityTypeResponse",
                }
            },
        ]

        return (await ActivityTypeMotor.aggregate(pipeline))[0]

    @classmethod
    async def update_activity_type(
        cls, activity_type_id: str, activity_type: ActivityType
    ):
        activity_type_db = ActivityTypeMotor(
            **activity_type.model_dump(
                by_alias=True, exclude={"_id", "id", "id_"}
            )
        )

        await activity_type_db.update(ObjectId(activity_type_id))

    @classmethod
    async def delete_activity_type(cls, activity_type_id: str):
        await ActivityTypeMotor.delete_one(_id=ObjectId(activity_type_id))
