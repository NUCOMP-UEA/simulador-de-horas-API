from typing import Optional, Type

from bson.objectid import ObjectId
from fastapi import HTTPException

from add_hours.application.dto.request.student import StudentRequest
from add_hours.application.dto.response.student import StudentResponse
from add_hours.domain.models.student.student import Student
from add_hours.domain.repository.student_repository_interface import (
    IStudentRepository,
)
from add_hours.utils.pydantic_object_id import PydanticObjectId


class StudentService:
    student_repository: Type[IStudentRepository]

    def __new__(cls, student_repository: Type[IStudentRepository]):
        cls.student_repository = student_repository
        return cls

    @classmethod
    async def save_student(
        cls, student_request: StudentRequest
    ) -> StudentResponse:
        student_id = PydanticObjectId(str(ObjectId()))

        await cls.student_repository.save(
            Student(**student_request.model_dump(), _id=student_id)
        )

        response = await cls.get_student(str(student_id))
        response._id = student_id

        return response

    @classmethod
    async def get_students(cls) -> list[StudentResponse]:
        return [
            StudentResponse(**student_info)
            for student_info in await cls.student_repository.get_students()
        ]

    @classmethod
    async def get_student(cls, student_id: str) -> Optional[StudentResponse]:
        if not ObjectId.is_valid(student_id):
            # TODO: Exception temporária
            raise HTTPException(status_code=422, detail="Invalid student id")

        student = await cls.student_repository.get_student(student_id)

        if student:
            return StudentResponse(**student)

    @classmethod
    async def student_exists(cls, student_id: str):
        if not ObjectId.is_valid(student_id):
            # TODO: Exception temporária
            raise HTTPException(status_code=422, detail="Invalid student id")

        return await cls.student_repository.student_exists(student_id)
