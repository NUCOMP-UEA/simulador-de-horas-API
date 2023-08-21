from add_hours.domain.models.activity.activity_type import ActivityType
from add_hours.domain.repository.activity_type_repository_interface import (
    IActivityTypeRepository,
)
from add_hours.infra.motor.activity.activity_type_model import ActivityTypeMotor


class ActivityTypeRepositoryMotor(IActivityTypeRepository):
    @classmethod
    async def save_activity_type(cls, activity_type: ActivityType):
        activity_type_db = ActivityTypeMotor(
            **activity_type.model_dump(exclude={"_id", "id_", "id"})
        )
        await activity_type_db.save()
