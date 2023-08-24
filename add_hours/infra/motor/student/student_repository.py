from bson.objectid import ObjectId

from add_hours.domain.models.activity.activity import Activity
from add_hours.domain.repository.student_repository_interface import (
    IStudentRepository,
)
from add_hours.infra.motor.student.student_model import StudentMotor


class StudentRepositoryMotor(IStudentRepository):
    @classmethod
    async def save(cls, activity: Activity):
        activity_db = StudentMotor(
            **activity.model_dump(by_alias=True),
        )
        await activity_db.save_student()

    @classmethod
    async def get_students(cls):
        return await StudentMotor.find_all()

    @classmethod
    async def get_student(cls, student_id: str):
        return await StudentMotor.find_one(_id=ObjectId(student_id))

    @classmethod
    async def student_exists(cls, student_id: str):
        return await StudentMotor.exists(_id=ObjectId(student_id))
