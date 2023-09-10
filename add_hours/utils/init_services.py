from add_hours.application.services.activity_service import ActivityService
from add_hours.application.services.activity_type_service import (
    ActivityTypeService,
)
from add_hours.application.services.auth_service import AuthService
from add_hours.application.services.storage_service import StorageService
from add_hours.application.services.student_service import StudentService
from add_hours.application.services.submit_service import SubmitService
from add_hours.infra.minio.storage_repository import StorageRepositoryMinio
from add_hours.infra.motor.activity.activity_repository import (
    ActivityRepositoryMotor,
)
from add_hours.infra.motor.activity.activity_type_repository import (
    ActivityTypeRepositoryMotor,
)
from add_hours.infra.motor.auth.auth_repository import AuthRepositoryMotor
from add_hours.infra.motor.student.student_repository import (
    StudentRepositoryMotor,
)
from add_hours.infra.smtp.SubmitRepository import SubmitRepository


def init_services():
    ActivityService(ActivityRepositoryMotor)
    ActivityTypeService(ActivityTypeRepositoryMotor)
    StudentService(StudentRepositoryMotor)
    AuthService(AuthRepositoryMotor)
    StorageService(StorageRepositoryMinio)
    SubmitService(SubmitRepository)
