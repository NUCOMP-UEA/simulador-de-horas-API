import json
import re

from unidecode import unidecode

from add_hours.domain.models.activity.activity_type import ActivityType
from add_hours.domain.repository.activity_type_repository_interface import (
    IActivityTypeRepository,
)
from add_hours.infra.motor.activity.activity_type_model import ActivityTypeMotor


class ActivityTypeRepositoryMotor(IActivityTypeRepository):
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
