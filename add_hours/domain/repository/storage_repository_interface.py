import io
from abc import ABC, abstractmethod


class IStorageRepository(ABC):
    @classmethod
    @abstractmethod
    async def save_certificate(
        cls, certificate_name: str, student_id: str, activity_id: str,
        certificate_bytes: io.BytesIO
    ):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_all_certificates(cls, student_id: str, activity_id: str):
        raise NotImplementedError()
