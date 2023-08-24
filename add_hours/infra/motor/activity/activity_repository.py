from datetime import datetime

from bson.objectid import ObjectId

from add_hours.domain.models.activity.activity import Activity
from add_hours.domain.repository.activity_repository_interface import (
    IActivityRepository,
)
from add_hours.infra.motor.activity.activity_model import ActivityMotor


class ActivityRepositoryMotor(IActivityRepository):
    @classmethod
    async def save_activity(cls, activity: Activity):
        activity_db = ActivityMotor(
            **activity.model_dump(
                exclude={"_id", "id_", "id", "date", "date_", "activity"},
                by_alias=True,
            ),
            date=datetime(
                day=activity.date_.day,
                month=activity.date_.month,
                year=activity.date_.year,
            ),
            activity=ObjectId(activity.activity)
        )
        await activity_db.save_activity()

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
