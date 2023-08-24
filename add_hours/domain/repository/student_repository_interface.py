from abc import ABC, abstractmethod

from add_hours.domain.models.student.student import Student


class IStudentRepository(ABC):
    @classmethod
    @abstractmethod
    async def save(cls, student: Student):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_students(cls):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_student(cls, student_id: str):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def student_exists(cls, student_id: str) -> bool:
        raise NotImplementedError()
