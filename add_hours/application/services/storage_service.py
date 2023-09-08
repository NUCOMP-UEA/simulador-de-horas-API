import io
from typing import Type

from fastapi import HTTPException

from add_hours.application.services.activity_service import ActivityService
from add_hours.application.services.student_service import StudentService
from add_hours.domain.repository.storage_repository_interface import \
    IStorageRepository


class StorageService:
    storage_repository: Type[IStorageRepository]

    def __new__(cls, storage_repository: Type[IStorageRepository]):
        cls.storage_repository = storage_repository
        return cls

    @classmethod
    async def save_certificate(
        cls, certificate_name: str, student_id: str, activity_id: str,
        certificate_bytes: io.BytesIO
    ):
        student_exists = await StudentService.student_exists(student_id)
        activity_exists = await ActivityService.activity_exists(activity_id)

        if not student_exists:
            raise HTTPException(status_code=404, detail="Student not found")

        if not activity_exists:
            raise HTTPException(status_code=404, detail="Activity not found")

        await cls.storage_repository.save_certificate(
            certificate_name, student_id, activity_id, certificate_bytes
        )

    @classmethod
    async def get_certificates(cls, student_id: str, activity_id: str):
        return await cls.storage_repository.get_all_certificates(
            student_id, activity_id
        )
