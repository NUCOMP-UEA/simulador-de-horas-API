from typing import Type

from fastapi import HTTPException

from add_hours.application.services.activity_service import ActivityService
from add_hours.application.services.activity_type_service import \
    ActivityTypeService
from add_hours.application.services.storage_service import StorageService
from add_hours.application.services.student_service import StudentService
from add_hours.application.services.utils.create_xlsx import create_xlsx
from add_hours.domain.models.student.student import Student
from add_hours.domain.repository.submit_repository_interface import \
    ISubmitRepository


class SubmitService:
    submit_repository: Type[ISubmitRepository]

    def __new__(
        cls, submit_repository: Type[ISubmitRepository]
    ):
        cls.submit_repository = submit_repository
        return cls

    @classmethod
    async def submit_email(cls, student_id: str):
        student_exists = await StudentService.student_exists(student_id)

        if not student_exists:
            raise HTTPException(status_code=404, detail="Student not found")

        student = Student(
            **((await StudentService.get_student(student_id)).model_dump(
                by_alias=True
            ))
        )
        # TODO: Requisitar um get_activities personalizado para este caso
        get_activities = await ActivityService.get_activities(
            student_id,
            1,
            1000000
        )

        activities = {}

        for activity in get_activities.activities:
            activities[activity.category] = (
                await ActivityTypeService.get_activity_type_by_id(
                    str(activity.category)
                )
            )

        table_xlsx_file = await create_xlsx(student, get_activities, activities)
        certificates_pdf = await StorageService.get_certificates(student_id)

        await cls.submit_repository.submit_email(
            student.name, student.enrollment, table_xlsx_file, certificates_pdf
        )
