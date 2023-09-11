import io
from typing import Type

from add_hours.application.exceptions.conflict import CertificateConflictStorage
from add_hours.domain.repository.storage_repository_interface import (
    IStorageRepository,
)


class StorageService:
    storage_repository: Type[IStorageRepository]

    def __new__(cls, storage_repository: Type[IStorageRepository]):
        cls.storage_repository = storage_repository
        return cls

    @classmethod
    async def save_certificate(
        cls,
        certificate_name: str,
        student_id: str,
        activity_id: str,
        certificate_bytes: io.BytesIO,
    ):
        response = await cls.storage_repository.save_certificate(
            certificate_name, student_id, activity_id, certificate_bytes
        )

        if not response:
            raise CertificateConflictStorage(
                "Certificate already issued for this activity and student",
            )

    @classmethod
    async def get_certificates(cls, student_id: str):
        (
            merged_pdfs,
            total_certificates,
        ) = await cls.storage_repository.get_all_certificates(student_id)
        return merged_pdfs, total_certificates

    @classmethod
    async def remove_certificate(cls, student_id: str, activity_id: str):
        await cls.storage_repository.remove_certificate(student_id, activity_id)
