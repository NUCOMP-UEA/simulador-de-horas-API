from add_hours.application.services.activity_service import ActivityService
from add_hours.application.services.activity_type_service import (
    ActivityTypeService,
)
from add_hours.infra.motor.activity.activity_repository import (
    ActivityRepositoryMotor,
)
from add_hours.infra.motor.activity.activity_type_repository import (
    ActivityTypeRepositoryMotor,
)


def init_services():
    ActivityService(ActivityRepositoryMotor)
    ActivityTypeService(ActivityTypeRepositoryMotor)
